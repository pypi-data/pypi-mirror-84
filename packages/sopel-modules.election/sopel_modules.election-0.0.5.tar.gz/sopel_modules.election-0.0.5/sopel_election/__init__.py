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
        'electoral_votes': 9,
    },
    'Alaska': {
        'code': 'AK',
        'presidential_race_id': '4299',
        'electoral_votes': 3,
    },
    'Arizona': {
        'code': 'AZ',
        'presidential_race_id': '4300',
        'electoral_votes': 11,
    },
    'Arkansas': {
        'code': 'AR',
        'presidential_race_id': '4301',
        'electoral_votes': 6,
    },
    'California': {
        'code': 'CA',
        'presidential_race_id': '4303',
        'electoral_votes': 55,
    },
    'Colorado': {
        'code': 'CO',
        'presidential_race_id': '4304',
        'electoral_votes': 9,
    },
    'Connecticut': {
        'code': 'CT',
        'presidential_race_id': '4305',
        'electoral_votes': 7,
    },
    'Delaware': {
        'code': 'DE',
        'presidential_race_id': '4306',
        'electoral_votes': 3,
    },
    'District of Columbia': {
        'code': 'DC',
        'presidential_race_id': '4308',
        'electoral_votes': 3,
    },
    'Florida': {
        'code': 'FL',
        'presidential_race_id': '4309',
        'electoral_votes': 29,
    },
    'Georgia': {
        'code': 'GA',
        'presidential_race_id': '4311',
        'electoral_votes': 16,
    },
    'Hawaii': {
        'code': 'HI',
        'presidential_race_id': '4312',
        'electoral_votes': 4,
    },
    'Idaho': {
        'code': 'ID',
        'presidential_race_id': '4313',
        'electoral_votes': 4,
    },
    'Illinois': {
        'code': 'IL',
        'presidential_race_id': '4314',
        'electoral_votes': 20,
    },
    'Indiana': {
        'code': 'IN',
        'presidential_race_id': '4315',
        'electoral_votes': 11,
    },
    'Iowa': {
        'code': 'IA',
        'presidential_race_id': '4316',
        'electoral_votes': 6,
    },
    'Kansas': {
        'code': 'KS',
        'presidential_race_id': '4317',
        'electoral_votes': 6,
    },
    'Kentucky': {
        'code': 'KY',
        'presidential_race_id': '4318',
        'electoral_votes': 8,
    },
    'Louisiana': {
        'code': 'LA',
        'presidential_race_id': '4319',
        'electoral_votes': 8,
    },
    'Maine': {
        'code': 'ME',
        'presidential_race_id': '4320',
        'electoral_votes': 4,
    },
    'Maryland': {
        'code': 'MD',
        'presidential_race_id': '4321',
        'electoral_votes': 10,
    },
    'Massachusetts': {
        'code': 'MA',
        'presidential_race_id': '4322',
        'electoral_votes': 11,
    },
    'Michigan': {
        'code': 'MI',
        'presidential_race_id': '4323',
        'electoral_votes': 16,
    },
    'Minnesota': {
        'code': 'MN',
        'presidential_race_id': '4324',
        'electoral_votes': 10,
    },
    'Mississippi': {
        'code': 'MS',
        'presidential_race_id': '4325',
        'electoral_votes': 6,
    },
    'Missouri': {
        'code': 'MO',
        'presidential_race_id': '4326',
        'electoral_votes': 10,
    },
    'Montana': {
        'code': 'MT',
        'presidential_race_id': '4327',
        'electoral_votes': 3,
    },
    'Nebraska': {
        'code': 'NE',
        'presidential_race_id': '4328',
        'electoral_votes': 5,
    },
    'Nevada': {
        'code': 'NV',
        'presidential_race_id': '4329',
        'electoral_votes': 6,
    },
    'New Hampshire': {
        'code': 'NH',
        'presidential_race_id': '4330',
        'electoral_votes': 4,
    },
    'New Jersey': {
        'code': 'NJ',
        'presidential_race_id': '4331',
        'electoral_votes': 14,
    },
    'New Mexico': {
        'code': 'NM',
        'presidential_race_id': '4332',
        'electoral_votes': 5,
    },
    'New York': {
        'code': 'NY',
        'presidential_race_id': '4333',
        'electoral_votes': 29,
    },
    'North Carolina': {
        'code': 'NC',
        'presidential_race_id': '4334',
        'electoral_votes': 15,
    },
    'North Dakota': {
        'code': 'ND',
        'presidential_race_id': '4335',
        'electoral_votes': 3,
    },
    'Ohio': {
        'code': 'OH',
        'presidential_race_id': '4336',
        'electoral_votes': 18,
    },
    'Oklahoma': {
        'code': 'OK',
        'presidential_race_id': '4337',
        'electoral_votes': 7,
    },
    'Oregon': {
        'code': 'OR',
        'presidential_race_id': '4338',
        'electoral_votes': 7,
    },
    'Pennsylvania': {
        'code': 'PA',
        'presidential_race_id': '4339',
        'electoral_votes': 20,
    },
    'Rhode Island': {
        'code': 'RI',
        'presidential_race_id': '4340',
        'electoral_votes': 4,
    },
    'South Carolina': {
        'code': 'SC',
        'presidential_race_id': '4341',
        'electoral_votes': 9,
    },
    'South Dakota': {
        'code': 'SD',
        'presidential_race_id': '4342',
        'electoral_votes': 3,
    },
    'Tennessee': {
        'code': 'TN',
        'presidential_race_id': '4343',
        'electoral_votes': 11,
    },
    'Texas': {
        'code': 'TX',
        'presidential_race_id': '4344',
        'electoral_votes': 38,
    },
    'Utah': {
        'code': 'UT',
        'presidential_race_id': '4345',
        'electoral_votes': 6,
    },
    'Vermont': {
        'code': 'VT',
        'presidential_race_id': '4346',
        'electoral_votes': 3,
    },
    'Virginia': {
        'code': 'VA',
        'presidential_race_id': '4347',
        'electoral_votes': 13,
    },
    'Washington': {
        'code': 'WA',
        'presidential_race_id': '4348',
        'electoral_votes': 12,
    },
    'West Virginia': {
        'code': 'WV',
        'presidential_race_id': '4349',
        'electoral_votes': 5,
    },
    'Wisconsin': {
        'code': 'WI',
        'presidential_race_id': '4350',
        'electoral_votes': 10,
    },
    'Wyoming': {
        'code': 'WY',
        'presidential_race_id': '4351',
        'electoral_votes': 3,
    },
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
        data = r.json()
        bot.say('General Election - '
                'Donald J. Trump {trump_electoral_votes} - '
                'Joe Biden {biden_electoral_votes} - '
                'Electoral Votes Remaining {electoral_votes_remaining} - '
                'Updated {updated_at}'
                .format(
                    trump_electoral_votes=sum([int(v[0]['e_votes']) for k, v in data['seats'].items()
                                               if k.isdigit()
                                               if v[0]['winner_party'].lower() in ['r', 'republican']]),
                    biden_electoral_votes=sum([int(v[0]['e_votes']) for k, v in data['seats'].items()
                                               if k.isdigit()
                                               if v[0]['winner_party'].lower() in ['d', 'democrat']]),
                    electoral_votes_remaining=sum([int(v[0]['e_votes']) for k, v in data['seats'].items()
                                                   if k.isdigit()
                                                   if v[0]['winner_party'] == '']),
                    updated_at=data['updated_at'],
                ))

        return
    else:
        # Allow multi state lookup (AK,AL,CA)
        for state in trigger.group(2).split(','):
            # Strip off space in comma split
            state = state.strip(' ')
            presidential_race_id = None

            # User provided state short code
            if len(state) == 2:
                for k, v in states.items():
                    if state.upper() == v['code']:
                        # Silently error if no state is found
                        if not states.get(k):
                            return NOLIMIT
                        # Set nicely formatted state for output
                        state = k
                        presidential_race_id = states.get(k)['presidential_race_id']
            # Otherwise, look up state by full name
            else:
                # Silently error if no state is found
                if not states.get(state.title()):
                    return NOLIMIT
                # Set nicely formatted state for output
                state = state.title()
                presidential_race_id = states.get(state.title())['presidential_race_id']

            # Get data for race
            r = requests.get(
                'https://www.270towin.com/election-results-live/php/race_results.php?race_id={presidential_race_id}'
                .format(presidential_race_id=presidential_race_id)
            )

            # Donald J. Trump 654,321 (69.9%) - Joe Biden 123,456 (12.3%) - 70.1% Reporting - Updated: Nov 03, 2020 12:38pm
            data = r.json()

            bot.say('{state} ({electoral_votes}) - '
                    'Donald J. Trump {trump_votes} ({trump_vote_percent}) - '
                    'Joe Biden {biden_votes} ({biden_vote_percent}) - '
                    '{precinct_percent} reporting - Updated {updated_at}'
                    .format(
                        state=state,
                        electoral_votes=states[state]['electoral_votes'],
                        trump_votes=data['candidate-5-votes'],
                        trump_vote_percent=data['candidate-5-vote_percent'],
                        biden_votes=data['candidate-11918-votes'],
                        biden_vote_percent=data['candidate-11918-vote_percent'],
                        precinct_percent=data['precinct_percent'],
                        updated_at=data['updated_at'],
                    ))
