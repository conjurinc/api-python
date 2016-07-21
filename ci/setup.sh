#!/usr/bin/env bash

conjur authn login -u admin -p secret

conjur resource create 'food:bacon'
conjur role create 'job:programmer'
conjur role create 'job:cook'

conjur resource permit  'food:bacon' 'job:cook' 'fry'
conjur resource permit 'food:bacon' 'job:programmer' 'eat'