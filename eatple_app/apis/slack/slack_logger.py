# Define

from eatple_app.define import *


def Slack_LogFollow(nickname):
    res = client.chat_postMessage(
        channel=SLACK_CHANNEL_EATPLE_LOG,
        text="{name}님이 잇플 채널을 팔로우햇쥐:mouse:".format(
            name=nickname
        )
    )

    return res


def Slack_LogUnfollow(nickname):
    res = client.chat_postMessage(
        channel=SLACK_CHANNEL_EATPLE_LOG,
        text="{name}님이 잇플 채널을 언팔로우햇..쥐:mouse:".format(
            name=nickname
        )
    )

    return res


def Slack_LogSignUp(user):
    res = client.chat_postMessage(
        channel=SLACK_CHANNEL_EATPLE_LOG,
        text="{name}님이 잇플에 들어옴, 흥폭발:face_with_hand_over_mouth:".format(
            name=user.nickname
        )
    )

    return res


def Slack_LogUsedOrder(order):
    if(settings.SETTING_ID == 'DEPLOY'):
        HOST_URL = 'https://eapi.eatple.com'
        DEV_LOG = ''
    else:
        HOST_URL = 'https://dev.eatple.com'
        DEV_LOG = '개발 서버에서 '

    if(order.type == ORDER_TYPE_NORMAL):
        res = client.chat_postMessage(
            channel=SLACK_CHANNEL_EATPLE_LOG,
            blocks=[
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "*{dev}{name}님이 잇플패스를 사용했습니다.*   :white_check_mark:\n"
                            "```\n"
                            "주문번호 [ <{host_url}/admin/eatple_app/order/{order_index}/change|{order_id}> ]\n"
                            " - 매장명 : {store}\n"
                            " - 메뉴명 : {menu}\n"
                            " - 픽업 시간 {pickup_time}\n\n"
                            " > <{host_url}/admin/eatple_app/order/{order_index}/change|주문 자세히 보기>\n"
                            "```"
                        ).format(
                            order_id=order.order_id,
                            dev=DEV_LOG,
                            name=order.ordersheet.user.nickname,
                            store=order.store,
                            menu=order.menu,
                            pickup_time=dateByTimeZone(order.pickup_time).strftime(
                                '%-m월 %-d일 %p %-I시 %-M분').replace('AM', '오전').replace('PM', '오후'),
                            host_url=HOST_URL,
                            order_index=order.id,
                        )
                    },
                },
                {
                    "type": "divider"
                },
            ]
        )
        return res

    else:
        res = client.chat_postMessage(
            channel=SLACK_CHANNEL_EATPLE_LOG,
            text="{name}님이 이상한 주문을 함"
        )
        return res


def Slack_LogPayOrder(order):
    if(settings.SETTING_ID == 'DEPLOY'):
        HOST_URL = 'https://eapi.eatple.com'
        DEV_LOG = ''
    else:
        HOST_URL = 'https://dev.eatple.com'
        DEV_LOG = '개발 서버에서 '

    if(order.type == ORDER_TYPE_NORMAL):
        res = client.chat_postMessage(
            channel=SLACK_CHANNEL_EATPLE_LOG,
            blocks=[
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "*{dev}{name}님이 일반 잇플패스를 발급함*   :label:\n"
                            "```\n"
                            "주문번호 [ <{host_url}/admin/eatple_app/order/{order_index}/change|{order_id}> ]\n"
                            " - 매장명 : {store}\n"
                            " - 메뉴명 : {menu}\n"
                            " - 픽업 시간 {pickup_time}\n\n"
                            " > <{host_url}/admin/eatple_app/order/{order_index}/change|주문 자세히 보기>\n"
                            "```"
                        ).format(
                            order_id=order.order_id,
                            dev=DEV_LOG,
                            name=order.ordersheet.user.nickname,
                            store=order.store,
                            menu=order.menu,
                            pickup_time=dateByTimeZone(order.pickup_time).strftime(
                                '%-m월 %-d일 %p %-I시 %-M분').replace('AM', '오전').replace('PM', '오후'),
                            host_url=HOST_URL,
                            order_index=order.id,
                        )
                    },
                },
                {
                    "type": "divider"
                },
            ]
        )
        return res

    elif(order.type == ORDER_TYPE_B2B):
        res = client.chat_postMessage(
            channel=SLACK_CHANNEL_EATPLE_LOG,
            blocks=[
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "*{dev}{name}님이 {company}에서 B2B 잇플패스를 발급함* :label:\n"
                            "```\n"
                            "주문번호 [ <{host_url}/admin/eatple_app/order/{order_index}/change|{order_id}> ]\n"
                            " - 매장명 : {store}\n"
                            " - 메뉴명 : {menu}\n"
                            " - 픽업 시간 {pickup_time}\n\n"
                            " > <{host_url}/admin/eatple_app/order/{order_index}/change|주문 자세히 보기>\n"
                            "```"
                        ).format(
                            order_id=order.order_id,
                            dev=DEV_LOG,
                            name=order.ordersheet.user.nickname,
                            company=order.ordersheet.user.company.name,
                            store=order.store,
                            menu=order.menu,
                            pickup_time=dateByTimeZone(order.pickup_time).strftime(
                                '%-m월 %-d일 %p %-I시 %-M분').replace('AM', '오전').replace('PM', '오후'),
                            host_url=HOST_URL,
                            order_index=order.id,
                        )
                    },
                    # "accessory": {
                    #    "type": "image",
                    #    "image_url": '{}{}'.format(HOST_URL, order.menu.imgURL()),
                    #    "alt_text": "menu"
                    # }
                },
                {
                    "type": "divider"
                },
            ]
        )
        return res

    elif(order.type == ORDER_TYPE_PROMOTION):
        res = client.chat_postMessage(
            channel=SLACK_CHANNEL_EATPLE_LOG,
            blocks=[
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "*{dev}{name}님이 프로모션 잇플패스를 발급함* :label:\n"
                            "```\n"
                            "주문번호 [ <{host_url}/admin/eatple_app/order/{order_index}/change|{order_id}> ]\n"
                            " - 매장명 : {store}\n"
                            " - 메뉴명 : {menu}\n"
                            " - 픽업 시간 {pickup_time}\n\n"
                            " > <{host_url}/admin/eatple_app/order/{order_index}/change|주문 자세히 보기>\n"
                            "```"
                        ).format(
                            order_id=order.order_id,
                            dev=DEV_LOG,
                            name=order.ordersheet.user.nickname,
                            store=order.store,
                            menu=order.menu,
                            pickup_time=dateByTimeZone(order.pickup_time).strftime(
                                '%-m월 %-d일 %p %-I시 %-M분').replace('AM', '오전').replace('PM', '오후'),
                            host_url=HOST_URL,
                            order_index=order.id,
                        )
                    },
                    # "accessory": {
                    #    "type": "image",
                    #    "image_url": '{}{}'.format(HOST_URL, order.menu.imgURL()),
                    #    "alt_text": "menu"
                    # }
                },
                {
                    "type": "divider"
                },
            ]
        )
        return res

    else:
        res = client.chat_postMessage(
            channel=SLACK_CHANNEL_EATPLE_LOG,
            text="{name}님이 이상한 주문을 함"
        )
        return res


def Slack_LogCancelOrder(order):
    if(settings.SETTING_ID == 'DEPLOY'):
        HOST_URL = 'https://eapi.eatple.com'
        DEV_LOG = ''
    else:
        HOST_URL = 'https://dev.eatple.com'
        DEV_LOG = '개발 서버에서 '

    res = client.chat_postMessage(
        channel=SLACK_CHANNEL_EATPLE_LOG,
        blocks=[
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        "*{dev}{name}님이 잇플패스를 취소함*   :bangbang:\n"
                        "```\n"
                        "주문번호 [ <{host_url}/admin/eatple_app/order/{order_index}/change|{order_id}> ]\n"
                        " - 매장명 : {store}\n"
                        " - 메뉴명 : {menu}\n"
                        " - 픽업 시간 {pickup_time}\n\n"
                        " > <{host_url}/admin/eatple_app/order/{order_index}/change|주문 자세히 보기>\n"
                        "```"
                    ).format(
                        order_id=order.order_id,
                        dev=DEV_LOG,
                        name=order.ordersheet.user.nickname,
                        store=order.store,
                        menu=order.menu,
                        pickup_time=dateByTimeZone(order.pickup_time).strftime(
                            '%-m월 %-d일 %p %-I시 %-M분').replace('AM', '오전').replace('PM', '오후'),
                        host_url=HOST_URL,
                        order_index=order.id,
                    )
                },
            },
            {
                "type": "divider"
            },
        ]
    )
    return res
