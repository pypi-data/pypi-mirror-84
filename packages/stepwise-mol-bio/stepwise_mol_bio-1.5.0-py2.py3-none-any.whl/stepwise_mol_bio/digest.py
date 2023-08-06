#!/usr/bin/env python3

"""\
Perform restriction digests using the protocol recommended by NEB.

Usage:
    digest <templates> <enzymes> [-d <ng>] [-D <ng/µL>] [-v <µL>] [-n <rxns>]
        [-g]

Arguments:
    <templates>
        The DNA to digest.  Use commas to specify multiple templates.  The 
        number of reactions will equal the number of templates.

    <enzymes>
        The restriction enzymes to use.  Only NEB enzymes are currently 
        supported.  If you are using an "HF" enzyme, specify that explicitly.  
        For example, "HindIII" and "HindIII-HF" have different protocols.  
        Enzyme names are case-insensitive, and multiple enzymes can be 
        specified using commas.

Options:
    -d --dna <µg>               [default: 1]
        The amount of DNA to digest, in µg.

    -D --dna-stock <ng/µL>      [default: 200]
        The stock concentration of the DNA template, in ng/µL.

    -v --target-volume <µL>     [default: 10]
        The ideal volume for the digestion reaction.  Note that the actual 
        reaction volume may be increased to ensure that the volume of enzyme 
        (which is determined by the amount of DNA to digest, see --dna) is less 
        than 10% of the total reaction volume, as recommended by NEB.

    -n --num-reactions <int>
        The number of reactions to setup.  By default, this is inferred from 
        the number of templates.

    -g --genomic
        Indicate that genomic DNA is being digested.  This will double the 
        amount of enzyme used, as recommended by NEB.
"""

import docopt
import stepwise
import autoprop
from pathlib import Path
from inform import Error, plural, did_you_mean
from stepwise_mol_bio import Main, app

@autoprop
class RestrictionDigest(Main):

    def __init__(self, templates, enzymes):
        self.templates = templates
        self.enzymes = enzymes

        self.dna_ug = 1
        self.dna_stock_nguL = 200
        self.target_volume_uL = 10
        self.num_reactions = None
        self.is_genomic = False

    @classmethod
    def from_docopt(cls, args):
        templates = [
                x.strip()
                for x in args['<templates>'].split(',')
        ]
        enzymes = [
                load_neb_enzyme(x)
                for x in args['<enzymes>'].split(',')
        ]

        self = cls(templates, enzymes)
        self.dna_ug = float(args['--dna'])
        self.dna_stock_nguL = float(args['--dna-stock'])
        self.target_volume_uL = float(args['--target-volume'])
        self.is_genomic = args['--genomic']

        if x := args['--num-reactions']:
            self.num_reactions = int(x)

        return self

    def get_reaction(self):
        # Define a prototypical restriction digest reaction.  Stock 
        # concentrations for BSA, SAM, and ATP come from the given catalog 
        # numbers.

        rxn = stepwise.MasterMix.from_text("""\
        Reagent  Catalog      Stock    Volume  MM?
        =======  =======  =========  ========  ===
        water                        to 50 µL  yes
        DNA               200 ng/µL      5 µL
        BSA        B9000   20 mg/mL      0 µL  yes
        SAM        B9003      32 mM      0 µL  yes
        ATP        P0756      10 mM      0 µL  yes
        buffer                  10x      5 µL  yes
        """)

        # Plug in the parameters the user requested.

        rxn.num_reactions = self.num_reactions or len(self.templates)

        rxn['DNA'].name = ','.join(self.templates)
        rxn['DNA'].hold_conc.stock_conc = self.dna_stock_nguL, 'ng/µL'
        
        for enz in self.enzymes:
            key = enz['name']
            stock = enz['concentration'] / 1000

            # The prototype reaction has 1 µg of DNA.  NEB recommends 10 U/µg 
            # (20 U/µg for genomic DNA), so set the initial enzyme volume 
            # according to that.  This will be adjusted later on.

            rxn[key].stock_conc = stock, 'U/µL'
            rxn[key].volume = (20 if self.is_genomic else 10) / stock, 'µL'
            rxn[key].master_mix = True

        rxn['buffer'].name = pick_compatible_buffer(self.enzymes)

        def add_supplement(key, unit, scale=1):
            conc = max(x['supplement'][key] for x in self.enzymes)

            if not conc:
                del rxn[key.upper()]
            else:
                rxn[key.upper()].hold_stock_conc.conc = conc * scale, unit

        add_supplement('bsa', 'mg/mL', 1e-3)
        add_supplement('sam', 'mM', 1e-3)
        add_supplement('atp', 'mM')
        
        # Update the reaction volume.  This takes some care, because the 
        # reaction volume depends on the enzyme volume, which in turn depends 
        # on the DNA quantity.

        k = self.dna_ug / 1  # The prototype reaction has 1 µg DNA.
        dna_vol = k * rxn['DNA'].volume
        enz_vols = {
                enz['name']: k * rxn[enz['name']].volume
                for enz in self.enzymes
        }
        enz_vol = sum(enz_vols.values())

        rxn.hold_ratios.volume = max(
                stepwise.Quantity(self.target_volume_uL, 'µL'),
                10 * enz_vol,

                # This is a bit of a hack.  The goal is to keep the water 
                # volume non-negative, but it won't necessarily work if there 
                # are supplements.
                10/9 * (dna_vol + enz_vol),
        )

        rxn['DNA'].volume = dna_vol
        for enz in self.enzymes:
            key = enz['name']
            rxn[key].volume = enz_vols[key]

        return rxn

    def get_protocol(self):
        from itertools import groupby
        from operator import itemgetter

        protocol = stepwise.Protocol()
        rxn = self.reaction
        rxn_type = (
                self.enzymes[0]['name']
                if len(self.enzymes) == 1 else
                'restriction'
        )

        def incubate(temp_getter, time_getter, time_formatter=lambda x: f'{x} min'):
            incubate_params = [
                    (k, max(time_getter(x) for x in group))
                    for k, group in groupby(self.enzymes, temp_getter)
            ]
            return '\n'.join(
                    f"- {temp}°C for {time_formatter(time)}"
                    for temp, time in sorted(incubate_params)
            )

        digest_steps = incubate(
                itemgetter('incubateTemp'),
                lambda x: 15 if x['timeSaver'] else 60,
                lambda x: '5–15 min' if x == 15 else '1 hour',
        )
        inactivate_steps = incubate(
                itemgetter('heatInactivationTemp'),
                itemgetter('heatInactivationTime'),
        )


        protocol += f"""\
Setup {plural(rxn.num_reactions):# {rxn_type} digestion/s} [1]:

{rxn}
"""

        protocol += f"""\
Incubate at the following temperatures [2]:

{digest_steps}
{inactivate_steps}
"""
        protocol.footnotes[1] = """\
NEB recommends 5–10 units of enzyme per µg DNA 
(10–20 units for genomic DNA).  Enzyme volume 
should not exceed 10% of the total reaction 
volume to prevent star activity due to excess 
glycerol.
"""
        protocol.footnotes[2] = """\
The heat inactivation step is not necessary if 
the DNA will be purified before use.
"""
        return protocol

class RestrictionDigestError(Error):
    pass

class CantDownloadEnzymes(RestrictionDigestError):
    template = """\
            Failed to download restriction enzyme data from NEB.  Make sure the 
            internet is connected and that the following URL is reachable:  

            {url}

            Note that the data only needs to be downloaded once.  After that, 
            this script should work offline."""
    wrap = True

    def __init__(self, url):
        super().__init__(url=url)


class UnknownEnzyme(RestrictionDigestError):
    template = "No such enzyme {enzyme_name!r}.  Did you mean {did_you_mean!r}?"
    wrap = True

    def __init__(self, enzyme_name, enzymes):
        super().__init__(
                enzyme_name=enzyme_name,
                enzymes=enzymes,
                did_you_mean=did_you_mean(enzyme_name, enzymes),
        )

def load_neb_enzyme(name):
    enzymes = load_neb_enzymes()
    enzymes_lower = {k.lower(): v for k, v in enzymes.items()}

    try:
        return enzymes_lower[name.lower()]
    except KeyError:
        raise UnknownEnzyme(name, enzymes)

def load_neb_enzymes():
    import json
    import requests

    cache = Path(app.user_cache_dir) / 'neb' / 'restriction_enzymes.json'
    cache.parent.mkdir(parents=True, exist_ok=True)

    try:
        url = 'http://nebcloner.neb.com/data/reprop.json'
        data = requests.get(url).json()

        with cache.open('w') as f:
            json.dump(data, f)

    except requests.exceptions.ConnectionError:
        if not cache.exists():
            raise NoEnzymeData(url)

        with cache.open() as f:
            data = json.load(f)

    return data

def pick_compatible_buffer(enzymes):
    if len(enzymes) == 1:
        return enzymes[0]['recommBuffer']

    # Don't consider `buf5`.  This is the code for buffers that are unique to a 
    # specific enzyme, so even if two enzymes both want `buf5`, it's not the 
    # same buffer.

    buffer_names = {
            '1': "NEBbuffer 1.1",
            '2': "NEBbuffer 2.1",
            '3': "NEBbuffer 3.1",
            '4': "CutSmart Buffer",
    }
    buffer_scores = {
            k: (
                sum(not x[f'star{k}'] for x in enzymes),  # Star activity?
                sum(x[f'buf{k}'] for x in enzymes),       # Cutting activity?
                k == '4',                                 # Prefer CutSmart
            )
            for k in buffer_names
    }
    best_buffer = max(
            buffer_scores,
            key=lambda k: buffer_scores[k],
    )

    return buffer_names[best_buffer]


if __name__ == '__main__':
    RestrictionDigest.main(__doc__)
