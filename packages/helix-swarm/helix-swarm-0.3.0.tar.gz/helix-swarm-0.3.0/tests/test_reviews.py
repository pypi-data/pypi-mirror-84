import re

import pytest
import responses

from helixswarm import (
    SwarmClient,
    SwarmCompatibleError,
    SwarmError,
    SwarmNotFoundError,
)


@responses.activate
def test_reviews_all():
    data = {
        'lastSeen': 12209,
        'reviews': [
            {
                'id': 12206,
                'author': 'swarm',
                'changes': [12205],
                'comments': 0,
                'commits': [],
                'commitStatus': [],
                'created': 1402507043,
                'deployDetails': [],
                'deployStatus': None,
                'description': 'Review Description\n',
                'participants': {
                    'swarm': []
                },
                'pending': True,
                'projects': [],
                'state': 'needsReview',
                'stateLabel': 'Needs Review',
                'testDetails': [],
                'testStatus': None,
                'type': 'default',
                'updated': 1402518492
            }
        ],
        'totalCount': 1
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews'),
        json=data
    )

    client = SwarmClient('http://server/api/v1', 'login', 'password')

    reviews = client.reviews.get()
    assert len(reviews['reviews']) == 1


@responses.activate
def test_reviews_all_parameters():
    data = {
        'lastSeen': 120,
        'reviews': [
            {
                'id': 123,
                'author': 'bruno',
                'description': 'Adding .jar that should have been included in r110\n',
                'state': 'needsReview'
            },
            {
                'id': 120,
                'author': 'bruno',
                'description': 'Fixing a typo.\n',
                'state': 'needsReview'
            }
        ],
        'totalCount': None
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews'),
        json=data
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    reviews = client.reviews.get(
        limit=2,
        fields=['id', 'description', 'author', 'state']
    )

    assert len(reviews['reviews']) == 2


def test_reviews_all_exceptions():
    client = SwarmClient('http://server/api/v1.2', 'login', 'password')

    # >= 2 API versions needed
    with pytest.raises(SwarmCompatibleError):
        client.reviews.get(authors=['p.belskiy'])


@responses.activate
def test_get_review_info():
    data = {
        'review': {
            'id': 12204,
            'author': 'bruno',
            'changes': [10667],
            'commits': [10667],
            'commitStatus': [],
            'created': 1399325913,
            'deployDetails': [],
            'deployStatus': None,
            'description': 'Adding .jar that should have been included in r10145\n',
            'participants': {
                'alex_qc': [],
                'bruno': {
                    'vote': 1,
                    'required': True
                },
                'vera': []
            },
            'reviewerGroups': {
                'group1': [],
                'group2': {
                    'required': True
                },
                'group3': {
                    'required': True,
                    'quorum': '1'
                }
            },
            'pending': False,
            'projects': {
                'swarm': ['main']
            },
            'state': 'archived',
            'stateLabel': 'Archived',
            'testDetails': {
                'url': 'http://jenkins.example.com/job/project_ci/123/'
            },
            'testStatus': None,
            'type': 'default',
            'updated': 1399325913
        }
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews/12204.*'),
        json=data
    )

    client = SwarmClient('http://server/api/v1', 'login', 'password')

    fields = [
        'id', 'author', 'changes', 'commits', 'commitStatus', 'created',
        'deployDetails', 'deployStatus', 'description', 'participants',
        'reviewerGroups', 'pending', 'projects', 'state', 'stateLabel',
        'testDetails', 'testStatus', 'type', 'updated'
    ]

    reviews = client.reviews.get_info(12204, fields=fields)
    assert reviews['review']['id'] == 12204


@responses.activate
def test_get_review_info_error():
    data = {
        'error': 'Not Found'
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews/12345'),
        json=data,
        status=404
    )

    client = SwarmClient('http://server/api/v1', 'login', 'password')
    with pytest.raises(SwarmNotFoundError):
        client.reviews.get_info(12345)


@responses.activate
def test_get_review_transitions():
    data = {
        'isValid': 'true',
        'transitions': {
            'needsRevision': 'Needs Revision',
            'approved': 'Approve',
            'approved:commit': 'Approve and Commit',
            'rejected': 'Reject',
            'archived': 'Archive'
        }
    }

    responses.add(
        responses.GET,
        re.compile(r'.*/api/v\d+/reviews/12345/transitions'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')
    response = client.reviews.get_transitions(
        12345,
        up_voters='bruno'
    )
    assert 'transitions' in response

    client = SwarmClient('http://server/api/v8', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client.reviews.get_transitions(12345)


@responses.activate
def test_create_review():
    data = {
        'review': {
            'id': 12205,
            'author': 'bruno',
            'changes': [10667],
            'commits': [10667],
            'commitStatus': [],
            'created': 1399325913,
            'deployDetails': [],
            'deployStatus': None,
            'description': 'My awesome description',
            'participants': {
                'bruno': []
            },
            'reviewerGroups': {
                'group1': [],
                'group2': {
                    'required': True
                },
                'group3': {
                    'required': True,
                    'quorum': '1'
                }
            },
            'pending': False,
            'projects': [],
            'state': 'archived',
            'stateLabel': 'Archived',
            'testDetails': [],
            'testStatus': None,
            'type': 'default',
            'updated': 1399325913
        }
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/reviews'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.reviews.create(
        10667,
        description='My awesome description',
        reviewers=['p.belskiy']
    )

    assert 'review' in response


@responses.activate
def test_update_review():
    data = {
        'review': {
            'id': 12306,
            'author': 'swarm',
            'changes': [12205],
            'comments': 0,
            'commits': [],
            'commitStatus': [],
            'created': 1402507043,
            'deployDetails': [],
            'deployStatus': None,
            'description': 'Updated Review Description\n',
            'participants': {
                'swarm': []
            },
            'pending': True,
            'projects': [],
            'state': 'needsReview',
            'stateLabel': 'Needs Review',
            'testDetails': [],
            'testStatus': None,
            'type': 'default',
            'updated': 1402518492
        },
        'transitions': {
            'needsRevision': 'Needs Revision',
            'approved': 'Approve',
            'rejected': 'Reject',
            'archived': 'Archive'
        },
        'canEditAuthor': True
    }

    responses.add(
        responses.PATCH,
        re.compile(r'.*/api/v\d+/reviews/12306'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.reviews.update(
        12306,
        author='new_author',
        description='new_description'
    )

    assert 'review' in response

    with pytest.raises(SwarmError):
        client.reviews.update(12306)


def test_create_review_exception():
    client_v1 = SwarmClient('http://server/api/v1', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client_v1.reviews.create(111, required_reviewers=['p.belskiy'])

    client_v6 = SwarmClient('http://server/api/v6', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client_v6.reviews.create(222, reviewer_groups=['master'])


@responses.activate
def test_archive_review():
    data = {
        'archivedReviews': [
            {
                'id': 911,
                'author': 'swarm',
                'changes': [601],
                'commits': [],
                'commitStatus': [],
                'created': 1461164344,
                'deployDetails': [],
                'deployStatus': None,
                'description': 'Touch up references on html pages.\n',
                'groups': [],
                'participants': {
                    'swarm': []
                },
                'pending': False,
                'projects': [],
                'state': 'archived',
                'stateLabel': 'Archived',
                'testDetails': [],
                'testStatus': None,
                'type': 'default',
                'updated': 1478191605
            },
            {
                'id': 908,
                'author': 'earl',
                'changes': [605],
                'commits': [],
                'commitStatus': [],
                'created': 1461947794,
                'deployDetails': [],
                'deployStatus': None,
                'description': 'Remove (attempted) installation of now deleted man pages.\n',
                'groups': [],
                'participants': {
                    'swarm': []
                },
                'pending': False,
                'projects': [],
                'state': 'archived',
                'stateLabel': 'Archived',
                'testDetails': [],
                'testStatus': None,
                'type': 'default',
                'updated': 1478191605
            }
        ],
        'failedReviews': [
            {}
        ]
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/reviews/archive'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.reviews.archive(
        not_updated_since='2016-06-30',
        description='My awesome description'
    )

    assert 'archivedReviews' in response

    client = SwarmClient('http://server/api/v5', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client.reviews.archive(
            not_updated_since='2016-06-30',
            description='My awesome description'
        )


@responses.activate
def test_cleanup_review():
    data = {
        'complete': [
            {
                '1': ['2']
            }
        ],
        'incomplete': []
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/reviews/12345/cleanup'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.reviews.cleanup(12345, reopen=True)
    assert 'complete' in response

    client = SwarmClient('http://server/api/v5', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client.reviews.cleanup(12345)


@responses.activate
def test_obliterate_review():
    data = {
        'isValid': True,
        'message': 'review 1 has been Obliterated',
        'code': 200
    }

    responses.add(
        responses.POST,
        re.compile(r'.*/api/v\d+/reviews/12345/obliterate'),
        json=data,
        status=200
    )

    client = SwarmClient('http://server/api/v9', 'login', 'password')

    response = client.reviews.obliterate(12345)
    assert 'message' in response

    client = SwarmClient('http://server/api/v8', 'login', 'password')
    with pytest.raises(SwarmCompatibleError):
        client.reviews.obliterate(12345)
