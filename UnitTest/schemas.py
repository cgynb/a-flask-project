# -*- coding: utf-8 -*-
# @Time    : 2022/4/22 10:15
# @Author  : CGY
# @File    : schemas.py
# @Project : NewWaiMai 
# @Comment : json schema
from jsonschema import validate
from pprint import pprint

# TagSchema

GET_TAG_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "status": {
            "type": "number",
            "enum": [200, 400]
        },
        "message": {
            "type": "string",
            "enum": ["success", "database error"]
        },
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["tag"],
                "properties": {
                    "tag": {
                        "type": "string"
                    }
                }
            }
        }
    }
}

POST_TAG_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "status": {
            "type": "number",
            "enum": [200, 400]
        },
        "message": {
            "type": "string",
            "enum": ["success", "please enter a tag", "database error"]
        }
    }
}

DELETE_TAG_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "status": {
            "type": "number",
            "enum": [200, 400]
        },
        "message": {
            "type": "string",
            "enum": ["success", "there is no such tag", "database error"]
        }
    }
}

# UserInfoSchema:


# FoodInfoSchema:
GET_SELF_OR_MERCHANT_FOOD_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "message": {
            "type": "string"
        },
        "status": {
            "type": "number",
            "enum": [200, 400]
        },
        "info": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["address", "food_desc", "food_id", "food_name", "food_price", "zans"],
                "properties": {
                    "address": {
                        "type": ["string", "null"]
                    },
                    "food_desc": {
                        "type": "string"
                    },
                    "food_id": {
                        "type": "number",
                        "multipleOf": 1
                    },
                    "food_name": {
                        "type": "string"
                    },
                    "food_price": {
                        "type": "number",
                        "multipleOf": 1
                    },
                    "zans": {
                        "type": "number",
                        "multipleOf": 1
                    }
                }
            }
        }
    }
}

GET_All_FOOD_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "message": {
            "type": "string"
        },
        "status": {
            "type": "number",
            "enum": [200, 400]
        },
        "info": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["foodid", "foodprice", "foodname",
                             "fooddesc", "zans", "ordernum",
                             "merchantid", "merchantname", "photo"],
                "properties": {
                    "photo": {
                        "type": ["string", "null"]
                    },
                    "fooddesc": {
                        "type": "string"
                    },
                    "foodid": {
                        "type": "number",
                        "multipleOf": 1
                    },
                    "foodname": {
                        "type": "string"
                    },
                    "foodprice": {
                        "type": "number",
                        "multipleOf": 1
                    },
                    "zans": {
                        "type": "number",
                        "multipleOf": 1
                    },
                    "ordernum": {
                        "type": "number",
                        "multipleOf": 1
                    },
                    "merchantid": {
                        "type": "number",
                        "multipleOf": 1
                    },
                    "merchantname": {
                        "type": "string"
                    }
                }
            }
        }
    }
}

POST_PUT_DELETE_FOOD_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "status": {
            "type": "number",
            "enum": [200, 400, 403]
        },
        "message": {
            "type": "string",
            "enum": ["success", "database error", "parameters error", "the food is not yours"]
        }
    }
}

# OrderInfoSchema:


# ZanApiSchema:
PUT_ZAN_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "status": {
            "type": "number",
            "enum": [200, 400, 404]
        },
        "message": {
            "type": "string",
            "enum": ["success", "lose some parameters", "database error", "food not found", "order not found",
                     "parameters error"]
        }
    }
}

# FollowSchema:
GET_FOLLOW_LIST_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "status": {
            "type": "number"
        },
        "message": {
            "type": "string"
        },
        "info": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [],
                "properties": {
                    "merchant_id": {
                        "type": "string"
                    },
                    "merchant_name": {
                        "type": "string"
                    },
                    "merchant_avatar": {
                        "type": "string"
                    },
                    "merchant_introduce": {
                        "type": "string"
                    }
                }
            }
        }
    }
}

GET_IF_FOLLOW_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "status": {
            "type": "number"
        },
        "message": {
            "type": "string"
        },
        "info": {
            "type": "string"
        }
    }
}

GET_MERCHANT_FOLLOW = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "status": {
            "type": "number"
        },
        "message": {
            "type": "string"
        },
        "follow-num": {
            "type": "number"
        }
    }
}

# CommentSchema:
GET_COMMENT_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "info": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["comment", "commentid", "replies", "useravatar", "username"],
                "properties": {
                    "comment": {
                        "type": "string"
                    },
                    "commentid": {
                        "type": "number"
                    },
                    "replies": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["reply", "subid", "useravatar", "username"],
                            "properties": {
                                "reply": {
                                    "type": "string"
                                },
                                "subid": {
                                    "type": "number"
                                },
                                "useravatar": {
                                    "type": ["string", "null"]
                                },
                                "username": {
                                    "type": "string"
                                }
                            }
                        }
                    },
                    "useravatar": {
                        "type": ["string", "null"]
                    },
                    "username": {
                        "type": "string"
                    }
                }
            }
        },
        "message": {
            "type": "string"
        },
        "status": {
            "type": "number"
        }
    }
}

POST_COMMENT_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "status": {
            "type": "number"
        },
        "message": {
            "type": "string"
        },
        "data": {
            "type": "object",
            "required": ["username", "useravatar"],
            "properties": {
                "comment": {
                    "type": "string"
                },
                "reply": {
                    "type": "string"
                },
                "username": {
                    "type": "string"
                },
                "useravatar": {
                    "type": "string"
                }
            }
        }
    }
}

PUT_DELETE_COMMENT_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "status": {
            "type": "number",
        },
        "message": {
            "type": "string"
        }
    }
}

# MessageSchema:
GET_ROOM_MSG_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["message", "send_msg_user", "user2", "user3", "user2_read", "user3_read"],
                "properties": {
                    "message": {
                        "type": "string"
                    },
                    "send_msg_user": {
                        "type": "number"
                    },
                    "user2": {
                        "type": "number"
                    },
                    "user2_read": {
                        "type": "boolean"
                    },
                    "user3": {
                        "type": "number"
                    },
                    "user3_read": {
                        "type": "boolean"
                    }
                }
            }
        },
        "message": {
            "type": "string"
        },
        "status": {
            "type": "number"
        },
        "userinfo": {
            "type": "object"
        }
    }
}
GET_SELF_MSG_SCHEMA = {
    "type": "object",
    "required": [],
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["lastMsg", "last_msg_sender", "room", "unread"],
                "properties": {
                    "lastMsg": {
                        "type": "string"
                    },
                    "last_msg_sender": {
                        "type": "string"
                    },
                    "room": {
                        "type": "string"
                    },
                    "unread": {
                        "type": "number"
                    }
                }
            }
        },
        "message": {
            "type": "string"
        },
        "status": {
            "type": "number"
        }
    }
}

# NoticeSchema:
GET_NOTICE_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "status": {
            "type": "number",
            "enum": [200, 400, 404]
        },
        "message": {
            "type": "string",
            "enum": ["success", "database error", "not found"]
        },
        "notice": {
            "type": "object",
            "required": ["title", "content"],
            "properties": {
                "title": {
                    "type": "string"
                },
                "content": {
                    "type": "string"
                }
            }
        }
    }
}

POST_NOTICE_SCHEMA = {
    "type": "object",
    "required": ["status", "message"],
    "properties": {
        "status": {
            "type": "number",
            "enum": [200, 400, 403]
        },
        "message": {
            "type": "string"
        },
    }
}
