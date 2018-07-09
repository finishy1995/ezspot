from lambda_function import lambda_handler

test_event_list = {
    "Records": [{
        "eventSource": "account:list",
        "user": "david.wang"
    }]
}

test_event_create = {
    "Records": [{
        "eventSource": "account:create",
        "user": "david.wang",
        "accounts": [{
            "account_name": "test1",
            "ak": "aaa",
            "sk": "bbb",
            "type": "AWS China",
            "timestamp": 111
        }]
    }]
}

test_event_update = {
    "Records": [{
        "eventSource": "account:update",
        "user": "david.wang",
        "accounts": [{
            "old_account_name": "test2",
            "account_name": "test3",
            "ak": "aaaac",
            "sk": "bbb",
            "type": "AWS China",
            "timestamp": 111
        }]
    }]
}

test_event_delete = {
    "Records": [{
        "eventSource": "account:delete",
        "user": "david.wang",
        "accounts": [{
            "account_name": "test",
        }]
    }]
}

print lambda_handler(test_event_delete, '')
