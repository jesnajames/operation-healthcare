transaction_response = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "1502": {
                        "summary": "Transaction ID: 1502",
                        "value": {
                            "message": {
                                "transaction_id": "1502",
                                "sku_name": "Baby Soap",
                                "sku_price": 68.2,
                                "transaction_datetime": "17/12/2021"
                            }
                        },
                    }
                }
            }
        }
    }
}

sku_summary_response = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "10 days": {
                        "summary": "Last 10 days",
                        "value": {
                            "message": [
                                {
                                    "sku_name": "Hand Sanitizer",
                                    "total_amount": 45
                                },
                                {
                                    "sku_name": "Hand Wash Liquid",
                                    "total_amount": 135
                                },
                                {
                                    "sku_name": "Shampoo",
                                    "total_amount": 699.99
                                },
                                {
                                    "sku_name": "Baby Soap",
                                    "total_amount": 34.1
                                }
                            ]
                        }
                    },
                    "30 days": {
                        "summary": "Last 30 days",
                        "value": {
                            "message": [
                                {
                                    "sku_name": "Hand Sanitizer",
                                    "total_amount": 45
                                },
                                {
                                    "sku_name": "Hand Wash Liquid",
                                    "total_amount": 135
                                },
                                {
                                    "sku_name": "Mouthwash",
                                    "total_amount": 499.98
                                },
                                {
                                    "sku_name": "Shampoo",
                                    "total_amount": 699.99
                                },
                                {
                                    "sku_name": "Baby Soap",
                                    "total_amount": 102.3
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
}

category_summary_response = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "10 days": {
                        "summary": "Last 10 days",
                        "value": {
                            "message": [
                                {
                                    "sku_category": "Hygiene",
                                    "total_amount": 180
                                },
                                {
                                    "sku_category": "Infant Care",
                                    "total_amount": 34.1
                                },
                                {
                                    "sku_category": "Personal Care",
                                    "total_amount": 949.98
                                }
                            ]
                        }
                    },
                    "30 days": {
                        "summary": "Last 30 days",
                        "value": {
                            "message": [
                                {
                                    "sku_category": "Hygiene",
                                    "total_amount": 180
                                },
                                {
                                    "sku_category": "Infant Care",
                                    "total_amount": 34.1
                                },
                                {
                                    "sku_category": "Personal Care",
                                    "total_amount": 1199.97
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
}
