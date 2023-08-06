# coding=utf8
"""sopel-election

Plugin for 2020 Presidential election results
"""
from __future__ import unicode_literals, absolute_import, division, print_function

import requests

from sopel import module
from sopel.module import commands, example, NOLIMIT

candidates = {
    'candidate-5': {
        'name': 'Donald J. Trump',
        'party': 'Republican',
    },
    'candidate-15587': {
        'name': 'Jesse Ventura',
        'party': 'Green',
    },
    'candidate-15586': {
        'name': 'Don Blankenship',
        'party': 'Constitution',
    },
    'candidate-15584': {
        'name': 'Brock Pierce',
        'party': 'Independent',
    },
    'candidate-12080': {
        'name': 'Jo Jorgensen',
        'party': 'Libertarian',
    },
    'candidate-11918': {
        'name': 'Joe Biden',
        'party': 'Democratic',
    },
    'candidate-2168': {
        'name': 'Roque De La Fuente',
        'party': 'Independent',
    }
}

states = {
    'Alabama': {
        'code': 'AL',
        'presidential_race_id': '4298',
    },
    'Alaska': {
        'code': 'AK',
        'presidential_race_id': '4299',
    },
    'Arizona': {
        'code': 'AZ',
        'presidential_race_id': '4300',
    },
    'Arkansas': {
        'code': 'AR',
        'presidential_race_id': '4301',
    },
    'California': {
        'code': 'CA',
        'presidential_race_id': '4303',
    },
    'Colorado': {
        'code': 'CO',
        'presidential_race_id': '4304',
    },
    'Connecticut': {
        'code': 'CT',
        'presidential_race_id': '4305',
    },
    'Delaware': {
        'code': 'DE',
        'presidential_race_id': '4306',
    },
    'District of Columbia': {
        'code': 'DC',
        'presidential_race_id': '4308',
    },
    'Florida': {
        'code': 'FL',
        'presidential_race_id': '4309',
    },
    'Georgia': {
        'code': 'GA',
        'presidential_race_id': '4311',
    },
    'Hawaii': {
        'code': 'HI',
        'presidential_race_id': '4312',
    },
    'Idaho': {
        'code': 'ID',
        'presidential_race_id': '4313',
    },
    'Illinois': {
        'code': 'IL',
        'presidential_race_id': '4314',
    },
    'Indiana': {
        'code': 'IN',
        'presidential_race_id': '4315',
    },
    'Iowa': {
        'code': 'IA',
        'presidential_race_id': '4316',
    },
    'Kansas': {
        'code': 'KS',
        'presidential_race_id': '4317',
    },
    'Kentucky': {
        'code': 'KY',
        'presidential_race_id': '4318',
    },
    'Louisiana': {
        'code': 'LA',
        'presidential_race_id': '4319',
    },
    'Maine': {
        'code': 'ME',
        'presidential_race_id': '4320',
    },
    'Maryland': {
        'code': 'MD',
        'presidential_race_id': '4321',
    },
    'Massachusetts': {
        'code': 'MA',
        'presidential_race_id': '4322',
    },
    'Michigan': {
        'code': 'MI',
        'presidential_race_id': '4323',
    },
    'Minnesota': {
        'code': 'MN',
        'presidential_race_id': '4324',
    },
    'Mississippi': {
        'code': 'MS',
        'presidential_race_id': '4325',
    },
    'Missouri': {
        'code': 'MO',
        'presidential_race_id': '4326',
    },
    'Montana': {
        'code': 'MT',
        'presidential_race_id': '4327',
    },
    'Nebraska': {
        'code': 'NE',
        'presidential_race_id': '4328',
    },
    'Nevada': {
        'code': 'NV',
        'presidential_race_id': '4329',
    },
    'New Hampshire': {
        'code': 'NH',
        'presidential_race_id': '4330',
    },
    'New Jersey': {
        'code': 'NJ',
        'presidential_race_id': '4331',
    },
    'New Mexico': {
        'code': 'NM',
        'presidential_race_id': '4332',
    },
    'New York': {
        'code': 'NY',
        'presidential_race_id': '4333',
    },
    'North Carolina': {
        'code': 'NC',
        'presidential_race_id': '4334',
    },
    'North Dakota': {
        'code': 'ND',
        'presidential_race_id': '4335',
    },
    'Ohio': {
        'code': 'OH',
        'presidential_race_id': '4336',
    },
    'Oklahoma': {
        'code': 'OK',
        'presidential_race_id': '4337',
    },
    'Oregon': {
        'code': 'OR',
        'presidential_race_id': '4338',
    },
    'Pennsylvania': {
        'code': 'PA',
        'presidential_race_id': '4339',
    },
    'Rhode Island': {
        'code': 'RI',
        'presidential_race_id': '4340',
    },
    'South Carolina': {
        'code': 'SC',
        'presidential_race_id': '4341',
    },
    'South Dakota': {
        'code': 'SD',
        'presidential_race_id': '4342',
    },
    'Tennessee': {
        'code': 'TN',
        'presidential_race_id': '4343',
    },
    'Texas': {
        'code': 'TX',
        'presidential_race_id': '4344',
    },
    'Utah': {
        'code': 'UT',
        'presidential_race_id': '4345',
    },
    'Vermont': {
        'code': 'VT',
        'presidential_race_id': '4346',
    },
    'Virginia': {
        'code': 'VA',
        'presidential_race_id': '4347',
    },
    'Washington': {
        'code': 'WA',
        'presidential_race_id': '4348',
    },
    'West Virginia': {
        'code': 'WV',
        'presidential_race_id': '4349',
    },
    'Wisconsin': {
        'code': 'WI',
        'presidential_race_id': '4350',
    },
    'Wyoming': {
        'code': 'WY',
        'presidential_race_id': '4351',
    }
}


def configure(config):
    pass


def setup(bot):
    pass


@module.commands('election')
def hello_world(bot, trigger):
    # Return total election results if no state provided
    if not trigger.group(2):
        r = requests.get(
            'https://www.270towin.com/election-results-live/php/get_presidential_results.php?election_year=2020')
        return
    else:
        state = trigger.group(2)
        presidential_race_id = None

        # User provided state short code
        if len(state) == 2:
            for k, v in states.items():
                if state.upper() == v['code']:
                    # Silently error if no state is found
                    if not states.get(k):
                        return NOLIMIT
                    presidential_race_id = states.get(k)['presidential_race_id']
        # Otherwise, look up state by full name
        else:
            # Silently error if no state is found
            if not states.get(state.title()):
                return NOLIMIT
            presidential_race_id = states.get(state.title())['presidential_race_id']

        # Get data for race
        r = requests.get(
            'https://www.270towin.com/election-results-live/php/race_results.php?race_id={presidential_race_id}'
            .format(presidential_race_id=presidential_race_id)
        )

        # Donald J. Trump 654,321 (69.9%) - Joe Biden 123,456 (12.3%) - 70.1% Reporting - Updated: Nov 03, 2020 12:38pm
        data = r.json()

        bot.say('Donald J. Trump {trump_votes} ({trump_vote_percent}) - '
                'Joe Biden {biden_votes} ({biden_vote_percent}) - '
                '{precinct_percent} - Updated {updated_at}'
                .format(
                    trump_votes=data['candidate-5-votes'],
                    trump_vote_percent=data['candidate-5-vote_percent'],
                    biden_votes=data['candidate-5-votes'],
                    biden_vote_percent=data['candidate-5-vote_percent'],
                    precinct_percent=data['precinct_percent'],
                    updated_at=data['updated_at'],
                ))
