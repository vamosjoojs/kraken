from app.integrations.reddit_integration import RedditIntegration


def get_reddit_users_to_send(
    tags,
    reddit_integration: RedditIntegration,
    stored_users_ids,
    limit: int
):
    users_to_send = []
    for tag in tags:
        tag, subreddit = tag.split(';')
        users_by_tag = reddit_integration.get_users(subreddit)
        if users_by_tag:
            for user in users_by_tag:
                if (
                    user not in stored_users_ids
                    and user not in users_to_send
                ):
                    users_to_send.append(user)
            if len(users_to_send) >= limit:
                break

    return users_to_send


def get_reddit_send_message_params(parameter_repo):
    messages_per_hour = 500
    sleep_per_send = 1
    users_per_round = 200

    parameters = parameter_repo.get_parameters()
    for parameter in parameters:
        if parameter.name == "reddit_messages_per_hour":
            messages_per_hour = parameter.int_value
        elif parameter.name == "reddit_sleep_per_send":
            sleep_per_send = parameter.int_value
        elif parameter.name == "reddit_users_per_round":
            users_per_round = parameter.int_value

    return messages_per_hour, sleep_per_send, users_per_round
