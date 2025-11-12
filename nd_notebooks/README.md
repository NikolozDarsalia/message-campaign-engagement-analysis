================================================================================
ENGINEERED FEATURES DOCUMENTATION
================================================================================

This document describes all features created through feature engineering for
email/push message campaign analysis.

================================================================================
"""

FEATURE_DOCUMENTATION = {
    
    # ========================================================================
    # 1. TEMPORAL FEATURES
    # ========================================================================
    "TEMPORAL_FEATURES": {
        "hour": {
            "description": "Hour of day when message was sent (0-23)",
            "calculation": "Extracted from sent_at timestamp",
            "use_case": "Identify optimal send times"
        },
        "weekday": {
            "description": "Day of week (0=Monday, 6=Sunday)",
            "calculation": "Extracted from sent_at timestamp",
            "use_case": "Understand weekly patterns"
        },
        "is_weekend": {
            "description": "Binary indicator if message sent on weekend",
            "calculation": "1 if weekday >= 5, else 0",
            "use_case": "Weekend vs weekday performance comparison"
        },
        "is_working_hours": {
            "description": "Binary indicator if sent during working hours (9-18)",
            "calculation": "1 if hour between 9 and 18, else 0",
            "use_case": "Business hours engagement patterns"
        },
        "days_since_last_msg": {
            "description": "Days elapsed since previous message to same client",
            "calculation": "Difference between current and previous sent_at per client",
            "use_case": "Measure message frequency and fatigue"
        },
        "days_since_last_email": {
            "description": "Days since last email to this client",
            "calculation": "Time difference for email channel only",
            "use_case": "Email-specific frequency analysis"
        },
        "days_since_last_push": {
            "description": "Days since last push notification to this client",
            "calculation": "Time difference for push channel only",
            "use_case": "Push notification frequency analysis"
        },
        "time_to_open_hours": {
            "description": "Hours between send and first open",
            "calculation": "(opened_first_time_at - sent_at) in hours",
            "use_case": "Measure engagement speed"
        },
        "time_to_click_hours": {
            "description": "Hours between send and first click",
            "calculation": "(clicked_first_time_at - sent_at) in hours",
            "use_case": "Measure conversion speed"
        }
    },
    
    # ========================================================================
    # 2. CHANNEL FEATURES
    # ========================================================================
    "CHANNEL_FEATURES": {
        "is_email": {
            "description": "Binary indicator for email channel",
            "calculation": "1 if channel_x == 'email', else 0",
            "use_case": "Channel-specific modeling"
        },
        "is_push": {
            "description": "Binary indicator for push notification",
            "calculation": "1 if channel_x == 'push', else 0",
            "use_case": "Channel-specific modeling"
        }
    },
    
    # ========================================================================
    # 3. CAMPAIGN TYPE FEATURES
    # ========================================================================
    "CAMPAIGN_TYPE_FEATURES": {
        "is_bulk": {
            "description": "Binary indicator for bulk campaign",
            "calculation": "1 if campaign_type == 'bulk', else 0",
            "use_case": "Mass marketing campaign identification"
        },
        "is_triggered": {
            "description": "Binary indicator for triggered campaign",
            "calculation": "1 if campaign_type == 'triggered', else 0",
            "use_case": "Behavioral trigger campaign identification"
        },
        "is_transactional": {
            "description": "Binary indicator for transactional message",
            "calculation": "1 if campaign_type == 'transactional', else 0",
            "use_case": "Transaction-related message identification"
        },
        "msg_position_in_campaign": {
            "description": "Sequential position of message within campaign for client",
            "calculation": "Cumulative count within (client_id, campaign_id) group",
            "use_case": "Track message series progression"
        }
    },
    
    # ========================================================================
    # 4. ROLLING MESSAGE VOLUME FEATURES (ANTI-LEAKAGE)
    # ========================================================================
    "ROLLING_VOLUME_FEATURES": {
        "sent_count_1d": {
            "description": "Number of messages sent to client in past 1 day",
            "calculation": "Rolling count over 1d window, closed='left' (excludes current)",
            "use_case": "Recent message frequency, fatigue detection"
        },
        "sent_count_1w": {
            "description": "Number of messages sent to client in past 7 days",
            "calculation": "Rolling count over 7d window, closed='left' (excludes current)",
            "use_case": "Recent message frequency, fatigue detection"
        },
        "sent_count_1m": {
            "description": "Number of messages sent to client in past 30 days",
            "calculation": "Rolling count over 30d window, closed='left'",
            "use_case": "Monthly message frequency"
        },
        "sent_count_email_1d": {
            "description": "Email messages to client in past day",
            "calculation": "Rolling sum of is_email over 1d, closed='left'",
            "use_case": "Email-specific frequency"
        },
        "sent_count_email_1w": {
            "description": "Email messages to client in past week",
            "calculation": "Rolling sum of is_email over 7d, closed='left'",
            "use_case": "Email-specific frequency"
        },
        "sent_count_email_1m": {
            "description": "Email messages to client in past month",
            "calculation": "Rolling sum of is_email over 30d, closed='left'",
            "use_case": "Monthly email frequency"
        },
        "sent_count_push_1d": {
            "description": "Push notifications to client in past day",
            "calculation": "Rolling sum of is_push over 1d, closed='left'",
            "use_case": "Push notification frequency"
        },
        "sent_count_push_1w": {
            "description": "Push notifications to client in past week",
            "calculation": "Rolling sum of is_push over 7d, closed='left'",
            "use_case": "Push notification frequency"
        },
        "sent_count_push_1m": {
            "description": "Push notifications to client in past month",
            "calculation": "Rolling sum of is_push over 30d, closed='left'",
            "use_case": "Monthly push frequency"
        },
        "avg_interval_1d": {
            "description": "Average days between messages in past day",
            "calculation": "Rolling mean of days_since_last_msg over 1d, closed='left'",
            "use_case": "Message pacing consistency"
        },
        "avg_interval_1w": {
            "description": "Average days between messages in past week",
            "calculation": "Rolling mean of days_since_last_msg over 7d, closed='left'",
            "use_case": "Message pacing consistency"
        },
        "avg_interval_1m": {
            "description": "Average days between messages in past month",
            "calculation": "Rolling mean of days_since_last_msg over 30d, closed='left'",
            "use_case": "Long-term message pacing"
        },
        "unique_campaigns_1d": {
            "description": "Number of distinct campaigns client received in past day",
            "calculation": "Rolling nunique of campaign_id over 1d, closed='left'",
            "use_case": "Campaign diversity exposure"
        },
        "unique_campaigns_1w": {
            "description": "Number of distinct campaigns client received in past week",
            "calculation": "Rolling nunique of campaign_id over 7d, closed='left'",
            "use_case": "Campaign diversity exposure"
        },
        "unique_campaigns_1m": {
            "description": "Number of distinct campaigns client received in past month",
            "calculation": "Rolling nunique of campaign_id over 30d, closed='left'",
            "use_case": "Monthly campaign variety"
        }
    },
    
    # ========================================================================
    # 5. ROLLING CAMPAIGN TYPE FEATURES
    # ========================================================================
    "ROLLING_CAMPAIGN_TYPE_FEATURES": {
        "bulk_count_1d": {
            "description": "Bulk campaigns received in past day",
            "calculation": "Rolling sum of is_bulk over 1d, closed='left'",
            "use_case": "Bulk campaign exposure"
        },
        "bulk_count_1w": {
            "description": "Bulk campaigns received in past week",
            "calculation": "Rolling sum of is_bulk over 7d, closed='left'",
            "use_case": "Bulk campaign exposure"
        },
        "bulk_count_1m": {
            "description": "Bulk campaigns received in past month",
            "calculation": "Rolling sum of is_bulk over 30d, closed='left'",
            "use_case": "Monthly bulk exposure"
        },
        "triggered_count_1d": {
            "description": "Triggered campaigns received in past day",
            "calculation": "Rolling sum of is_triggered over 1d, closed='left'",
            "use_case": "Behavioral trigger exposure"
        },
        "triggered_count_1w": {
            "description": "Triggered campaigns received in past week",
            "calculation": "Rolling sum of is_triggered over 7d, closed='left'",
            "use_case": "Behavioral trigger exposure"
        },
        "triggered_count_1m": {
            "description": "Triggered campaigns received in past month",
            "calculation": "Rolling sum of is_triggered over 30d, closed='left'",
            "use_case": "Monthly triggered exposure"
        },
        "transactional_count_1d": {
            "description": "Transactional messages received in past day",
            "calculation": "Rolling sum of is_transactional over 1d, closed='left'",
            "use_case": "Transaction message frequency"
        },
        "transactional_count_1w": {
            "description": "Transactional messages received in past week",
            "calculation": "Rolling sum of is_transactional over 7d, closed='left'",
            "use_case": "Transaction message frequency"
        },
        "transactional_count_1m": {
            "description": "Transactional messages received in past month",
            "calculation": "Rolling sum of is_transactional over 30d, closed='left'",
            "use_case": "Monthly transaction messages"
        }
    },
    
    # ========================================================================
    # 6. SUBJECT LINE FEATURES (ROLLING)
    # ========================================================================
    "SUBJECT_LINE_FEATURES": {
        "avg_subject_len_1d": {
            "description": "Average subject line length in past day",
            "calculation": "Rolling mean of subject_length over 1d, closed='left'",
            "use_case": "Subject length consistency"
        },        
        "avg_subject_len_1w": {
            "description": "Average subject line length in past week",
            "calculation": "Rolling mean of subject_length over 7d, closed='left'",
            "use_case": "Subject length consistency"
        },
        "avg_subject_len_1m": {
            "description": "Average subject line length in past month",
            "calculation": "Rolling mean of subject_length over 30d, closed='left'",
            "use_case": "Long-term subject length patterns"
        },
        "subject_personalization_prop_1d": {
            "description": "Proportion of subjects with personalization in past day",
            "calculation": "Rolling mean of subject_with_personalization over 1d",
            "use_case": "Personalization exposure"
        },
        "subject_personalization_prop_1w": {
            "description": "Proportion of subjects with personalization in past week",
            "calculation": "Rolling mean of subject_with_personalization over 7d",
            "use_case": "Personalization exposure"
        },
        "subject_personalization_prop_1m": {
            "description": "Proportion of subjects with personalization in past month",
            "calculation": "Rolling mean of subject_with_personalization over 30d",
            "use_case": "Monthly personalization rate"
        },
        "subject_bonuses_prop_1d": {
            "description": "Proportion of subjects mentioning bonuses in past day",
            "calculation": "Rolling mean of subject_with_bonuses over 1d",
            "use_case": "Bonus offer frequency"
        },
        "subject_bonuses_prop_1w": {
            "description": "Proportion of subjects mentioning bonuses in past week",
            "calculation": "Rolling mean of subject_with_bonuses over 7d",
            "use_case": "Bonus offer frequency"
        },
        "subject_bonuses_prop_1m": {
            "description": "Proportion of subjects mentioning bonuses in past month",
            "calculation": "Rolling mean of subject_with_bonuses over 30d",
            "use_case": "Bonus offer frequency"
        },
        "subject_discount_prop_1d": {
            "description": "Proportion of subjects with discount mentions in past day",
            "calculation": "Rolling mean of subject_with_discount over 1d",
            "use_case": "Discount promotion exposure"
        },
        "subject_discount_prop_1w": {
            "description": "Proportion of subjects with discount mentions in past week",
            "calculation": "Rolling mean of subject_with_discount over 7d",
            "use_case": "Discount promotion exposure"
        },
        "subject_discount_prop_1m": {
            "description": "Proportion of subjects with discount mentions in past month",
            "calculation": "Rolling mean of subject_with_discount over 30d",
            "use_case": "Discount promotion exposure"
        },
        "subject_deadline_prop_1d": {
            "description": "Proportion of subjects with urgency/deadline in past day",
            "calculation": "Rolling mean of subject_with_deadline over 1d",
            "use_case": "Urgency tactic frequency"
        },
        "subject_deadline_prop_1w": {
            "description": "Proportion of subjects with urgency/deadline in past week",
            "calculation": "Rolling mean of subject_with_deadline over 7d",
            "use_case": "Urgency tactic frequency"
        },
        "subject_deadline_prop_1w": {
            "description": "Proportion of subjects with urgency/deadline in past month",
            "calculation": "Rolling mean of subject_with_deadline over 30d",
            "use_case": "Urgency tactic frequency"
        },
        "subject_emoji_prop_1d": {
            "description": "Proportion of subjects with emoji in past day",
            "calculation": "Rolling mean of subject_with_emoji over 1d",
            "use_case": "Emoji usage patterns"
        }
        "subject_emoji_prop_1w": {
            "description": "Proportion of subjects with emoji in past week",
            "calculation": "Rolling mean of subject_with_emoji over 7d",
            "use_case": "Emoji usage patterns"
        }
        "subject_emoji_prop_1m": {
            "description": "Proportion of subjects with emoji in past month",
            "calculation": "Rolling mean of subject_with_emoji over 30d",
            "use_case": "Emoji usage patterns"
        }
    },
    
    # ========================================================================
    # 7. TEMPORAL PATTERN FEATURES (ROLLING)
    # ========================================================================
    "TEMPORAL_PATTERN_FEATURES": {
        "weekend_ratio_1w": {
            "description": "Proportion of messages sent on weekends in past week",
            "calculation": "Rolling mean of is_weekend over 7d, closed='left'",
            "use_case": "Weekend sending patterns"
        },
        "weekend_ratio_1m": {
            "description": "Proportion of messages sent on weekends in past month",
            "calculation": "Rolling mean of is_weekend over 30d, closed='left'",
            "use_case": "Monthly weekend patterns"
        },
        "working_hours_ratio_1d": {
            "description": "Proportion sent during working hours in past day",
            "calculation": "Rolling mean of is_working_hours over 1d, closed='left'",
            "use_case": "Business hours sending patterns"
        },
        "working_hours_ratio_1w": {
            "description": "Proportion sent during working hours in past week",
            "calculation": "Rolling mean of is_working_hours over 7d, closed='left'",
            "use_case": "Business hours sending patterns"
        },
        "working_hours_ratio_1m": {
            "description": "Proportion sent during working hours in past month",
            "calculation": "Rolling mean of is_working_hours over 30d, closed='left'",
            "use_case": "Monthly business hours patterns"
        }
    },
    
    # ========================================================================
    # 8. A/B TEST AND WARM-UP FEATURES
    # ========================================================================
    "AB_TEST_FEATURES": {
        "ab_test_count_1d": {
            "description": "Number of A/B test messages in past day",
            "calculation": "Rolling sum of ab_test over 1d, closed='left'",
            "use_case": "A/B test exposure tracking"
        },
        "ab_test_count_1w": {
            "description": "Number of A/B test messages in past week",
            "calculation": "Rolling sum of ab_test over 7d, closed='left'",
            "use_case": "A/B test exposure tracking"
        },
        "ab_test_count_1m": {
            "description": "Number of A/B test messages in past month",
            "calculation": "Rolling sum of ab_test over 30d, closed='left'",
            "use_case": "Monthly A/B test frequency"
        },
        "warmup_mode_count_1d": {
            "description": "Number of warm-up mode messages in past day",
            "calculation": "Rolling sum of warmup_mode over 1d, closed='left'",
            "use_case": "Warm-up phase tracking"
        },
        "warmup_mode_count_1w": {
            "description": "Number of warm-up mode messages in past week",
            "calculation": "Rolling sum of warmup_mode over 7d, closed='left'",
            "use_case": "Warm-up phase tracking"
        },
        "warmup_mode_count_1m": {
            "description": "Number of warm-up mode messages in past month",
            "calculation": "Rolling sum of warmup_mode over 30d, closed='left'",
            "use_case": "Monthly warm-up exposure"
        }
    },
    
    # ========================================================================
    # 9. MARKET-LEVEL FEATURES
    # ========================================================================
    "MARKET_LEVEL_FEATURES": {
        "total_msgs": {
            "description": "Total messages sent across all clients in current hour",
            "calculation": "Count of messages per hour bucket",
            "use_case": "Market-level activity indicator"
        },
        "market_avg_msgs_6h": {
            "description": "Average hourly messages in past 6 hours (market-wide)",
            "calculation": "Rolling mean of total_msgs over 6H, closed='left'",
            "use_case": "Short-term market activity"
        },
        "market_avg_msgs_1d": {
            "description": "Average hourly messages in past day (market-wide)",
            "calculation": "Rolling mean of total_msgs over 1D, closed='left'",
            "use_case": "Daily market activity"
        },
        "market_avg_msgs_1w": {
            "description": "Average hourly messages in past week (market-wide)",
            "calculation": "Rolling mean of total_msgs over 7D, closed='left'",
            "use_case": "Weekly market trends"
        },
        "market_avg_msgs_1m": {
            "description": "Average hourly messages in past month (market-wide)",
            "calculation": "Rolling mean of total_msgs over 30D, closed='left'",
            "use_case": "Long-term market baseline"
        }
    },
    
    # ========================================================================
    # 10. LAGGED ENGAGEMENT FEATURES (ANTI-LEAKAGE)
    # ========================================================================
    "LAGGED_ENGAGEMENT_FEATURES": {
        "is_opened_prev": {
            "description": "Whether previous message was opened",
            "calculation": "Shifted is_opened by 1 position per client",
            "use_case": "Previous engagement indicator, prevents leakage"
        },
        "is_clicked_prev": {
            "description": "Whether previous message was clicked",
            "calculation": "Shifted is_clicked by 1 position per client",
            "use_case": "Previous click behavior"
        },
        "is_purchased_prev": {
            "description": "Whether previous message led to purchase",
            "calculation": "Shifted is_purchased by 1 position per client",
            "use_case": "Previous conversion indicator"
        },
        "time_to_open_hours_prev": {
            "description": "Hours to open for previous message",
            "calculation": "Shifted time_to_open_hours by 1 position per client",
            "use_case": "Previous engagement speed"
        }
    },
    
    # ========================================================================
    # 11. ROLLING ENGAGEMENT RATES (ANTI-LEAKAGE)
    # ========================================================================
    "ROLLING_ENGAGEMENT_RATES": {
        "is_opened_rate_1w": {
            "description": "Open rate over past week (excluding current message)",
            "calculation": "Rolling mean of is_opened_prev over 7d, closed='left'",
            "use_case": "Recent open behavior, no leakage"
        },
        "is_opened_rate_1m": {
            "description": "Open rate over past month (excluding current message)",
            "calculation": "Rolling mean of is_opened_prev over 30d, closed='left'",
            "use_case": "Long-term open behavior"
        },
        "is_clicked_rate_1w": {
            "description": "Click rate over past week (excluding current message)",
            "calculation": "Rolling mean of is_clicked_prev over 7d, closed='left'",
            "use_case": "Recent click behavior"
        },
        "is_clicked_rate_1m": {
            "description": "Click rate over past month (excluding current message)",
            "calculation": "Rolling mean of is_clicked_prev over 30d, closed='left'",
            "use_case": "Long-term click behavior"
        },
        "is_purchased_rate_1w": {
            "description": "Purchase rate over past week (excluding current message)",
            "calculation": "Rolling mean of is_purchased_prev over 7d, closed='left'",
            "use_case": "Recent conversion behavior"
        },
        "is_purchased_rate_1m": {
            "description": "Purchase rate over past month (excluding current message)",
            "calculation": "Rolling mean of is_purchased_prev over 30d, closed='left'",
            "use_case": "Long-term conversion behavior"
        }
    },
    
    # ========================================================================
    # 12. BAYESIAN SMOOTHED RATES (ANTI-LEAKAGE)
    # ========================================================================
    "BAYESIAN_SMOOTHED_RATES": {
        "is_opened_rate_prev_smooth": {
            "description": "Smoothed historical open rate (Bayesian shrinkage)",
            "calculation": "(cumsum_prev + α*global_rate) / (trials + α + β)",
            "use_case": "Stable open rate estimate, handles low counts"
        },
        "is_clicked_rate_prev_smooth": {
            "description": "Smoothed historical click rate (Bayesian shrinkage)",
            "calculation": "(cumsum_prev + α*global_rate) / (trials + α + β)",
            "use_case": "Stable click rate estimate, handles low counts"
        },
        "is_purchased_rate_prev_smooth": {
            "description": "Smoothed historical purchase rate (Bayesian shrinkage)",
            "calculation": "(cumsum_prev + α*global_rate) / (trials + α + β)",
            "use_case": "Stable conversion rate estimate, handles low counts"
        }
    },
    
    # ========================================================================
    # 13. CAMPAIGN-LEVEL QUALITY FEATURES
    # ========================================================================
    "CAMPAIGN_QUALITY_FEATURES": {
        "is_opened_rate_campaign_per_client": {
            "description": "Historical open rate for this campaign (for this client)",
            "calculation": "Expanding mean of is_opened shifted by 1, per (client, campaign)",
            "use_case": "Campaign-specific open performance"
        },
        "is_clicked_rate_campaign_per_client": {
            "description": "Historical click rate for this campaign (for this client)",
            "calculation": "Expanding mean of is_clicked shifted by 1, per (client, campaign)",
            "use_case": "Campaign-specific click performance"
        },
        "is_purchased_rate_campaign_per_client": {
            "description": "Historical purchase rate for this campaign (for this client)",
            "calculation": "Expanding mean of is_purchased shifted by 1, per (client, campaign)",
            "use_case": "Campaign-specific conversion performance"
        }
        "is_opened_rate_campaign": {
            "description": "Historical open rate for this campaign",
            "calculation": "Expanding mean of is_opened shifted by 1, per (campaign)",
            "use_case": "Campaign-specific open performance"
        },
        "is_clicked_rate_campaign": {
            "description": "Historical click rate for this campaign",
            "calculation": "Expanding mean of is_clicked shifted by 1, per (campaign)",
            "use_case": "Campaign-specific click performance"
        },
        "is_purchased_rate_campaign": {
            "description": "Historical purchase rate for this campaign",
            "calculation": "Expanding mean of is_purchased shifted by 1, per (campaign)",
            "use_case": "Campaign-specific conversion performance"
        }
    },
    
    # ========================================================================
    # 14. CUSTOMER EXPECTATION GAP FEATURES
    # ========================================================================
    "EXPECTATION_GAP_FEATURES": {
        "is_opened_expect_gap_1w": {
            "description": "Gap between recent (1w) and long-term open behavior",
            "calculation": "is_opened_rate_1w - is_opened_rate_prev_smooth",
            "use_case": "Detect recent behavior changes (fatigue/revival)"
        },
        "is_opened_expect_gap_1m": {
            "description": "Gap between recent (1m) and long-term open behavior",
            "calculation": "is_opened_rate_1m - is_opened_rate_prev_smooth",
            "use_case": "Monthly behavior deviation"
        },
        "is_opened_expect_gap_overall": {
            "description": "Gap between overall average and smoothed open rate",
            "calculation": "client_avg_is_opened - is_opened_rate_prev_smooth",
            "use_case": "Overall engagement vs baseline"
        },
        "is_clicked_expect_gap_1w": {
            "description": "Gap between recent (1w) and long-term click behavior",
            "calculation": "is_clicked_rate_1w - is_clicked_rate_prev_smooth",
            "use_case": "Recent click behavior change"
        },
        "is_clicked_expect_gap_1m": {
            "description": "Gap between recent (1m) and long-term click behavior",
            "calculation": "is_clicked_rate_1m - is_clicked_rate_prev_smooth",
            "use_case": "Monthly click behavior deviation"
        },
        "is_clicked_expect_gap_overall": {
            "description": "Gap between overall average and smoothed click rate",
            "calculation": "client_avg_is_clicked - is_clicked_rate_prev_smooth",
            "use_case": "Overall click engagement vs baseline"
        },
        "is_purchased_expect_gap_1w": {
            "description": "Gap between recent (1w) and long-term purchase behavior",
            "calculation": "is_purchased_rate_1w - is_purchased_rate_prev_smooth",
            "use_case": "Recent conversion change"
        },
        "is_purchased_expect_gap_1m": {
            "description": "Gap between recent (1m) and long-term purchase behavior",
            "calculation": "is_purchased_rate_1m - is_purchased_rate_prev_smooth",
            "use_case": "Monthly conversion deviation"
        },
        "is_purchased_expect_gap_overall": {
            "description": "Gap between overall average and smoothed purchase rate",
            "calculation": "client_avg_is_purchased - is_purchased_rate_prev_smooth",
            "use_case": "Overall conversion vs baseline"
        }
    }

    # ========================================================================
    # 15. Global Company Performance Features
    # ========================================================================
    "GLOBAL_COMPANY_PERFORMANCE_FEATURES": {
        "global_is_opened_rate_1d": {
            "description": "Open rate for the last 1 day",
            "calculation": "Rolling mean of is_opened over 1d, closed='left'",
            "use_case": "Detect costumers relationship to the company for the recent period"
        },
        "global_is_opened_rate_1w": {
            "description": "Open rate for the last 1 week",
            "calculation": "Rolling mean of is_opened over 1w, closed='left'",
            "use_case": "Detect costumers relationship to the company for the recent period"
        },
        "global_is_opened_rate_1m": {
            "description": "Open rate for the last 1 month",
            "calculation": "Rolling mean of is_opened over 1m, closed='left'",
            "use_case": "Detect costumers relationship to the company for the recent period"
        },
        "global_is_clicked_rate_1d": {
            "description": "Click rate for the last 1 day",
            "calculation": "Rolling mean of is_clicked over 1d, closed='left'",
            "use_case": "Detect costumers relationship to the company for the recent period"
        },
        "global_is_clicked_rate_1w": {
            "description": "Click rate for the last 1 week",
            "calculation": "Rolling mean of is_clicked over 1w, closed='left'",
            "use_case": "Detect costumers relationship to the company for the recent period"
        },
        "global_is_opened_rate_1m": {
            "description": "Click rate for the last 1 month",
            "calculation": "Rolling mean of is_clicked over 1m, closed='left'",
            "use_case": "Detect costumers relationship to the company for the recent period"
        },
        "global_is_purchased_rate_1d": {
            "description": "Purchase rate for the last 1 day",
            "calculation": "Rolling mean of is_purchase over 1d, closed='left'",
            "use_case": "Detect costumers relationship to the company for the recent period"
        },
        "global_is_purchased_rate_1w": {
            "description": "Purchase rate for the last 1 week",
            "calculation": "Rolling mean of is_purchase over 1w, closed='left'",
            "use_case": "Detect costumers relationship to the company for the recent period"
        },
        "global_is_purchased_rate_1m": {
            "description": "Purchase rate for the last 1 month",
            "calculation": "Rolling mean of is_purchase over 1m, closed='left'",
            "use_case": "Detect costumers relationship to the company for the recent period"
        },
    }    

    # ========================================================================
    # 16. Client engagement deviation from overall engagement of the company
    # ========================================================================
    "CLIENT_EXPECTATION_DEVIATION_FEATURES": {
        "open_deviation_1d": {
            "description": "Client-level open rate deviation from the company-wide average for the previous 1 day",
            "calculation": "(Client open rate over 1d − Global open rate over 1d) / Global open rate over 1d, using closed='left'",
            "use_case": "Measures how much more or less engaged a client is compared to the average customer over the past day"
        },
        "open_deviation_1w": {
            "description": "Client-level open rate deviation from the company-wide average for the previous 1 week",
            "calculation": "(Client open rate over 7d − Global open rate over 7d) / Global open rate over 7d, using closed='left'",
            "use_case": "Identifies short-term engagement divergence compared to global campaign trends"
        },
        "open_deviation_1m": {
            "description": "Client-level open rate deviation from the company-wide average for the previous 1 month",
            "calculation": "(Client open rate over 30d − Global open rate over 30d) / Global open rate over 30d, using closed='left'",
            "use_case": "Captures medium-term engagement divergence, showing sustained over- or under-engagement"
        },

        "click_deviation_1d": {
            "description": "Client-level click rate deviation from the company-wide average for the previous 1 day",
            "calculation": "(Client click rate over 1d − Global click rate over 1d) / Global click rate over 1d, using closed='left'",
            "use_case": "Detects how much a client's short-term click activity differs from the global audience behavior"
        },
        "click_deviation_1w": {
            "description": "Client-level click rate deviation from the company-wide average for the previous 1 week",
            "calculation": "(Client click rate over 7d − Global click rate over 7d) / Global click rate over 7d, using closed='left'",
            "use_case": "Highlights short-term differences between individual and overall engagement patterns"
        },
        "click_deviation_1m": {
            "description": "Client-level click rate deviation from the company-wide average for the previous 1 month",
            "calculation": "(Client click rate over 30d − Global click rate over 30d) / Global click rate over 30d, using closed='left'",
            "use_case": "Evaluates whether the client’s click engagement trend aligns with or diverges from the overall market behavior"
        },

        "purchase_deviation_1d": {
            "description": "Client-level purchase rate deviation from the company-wide average for the previous 1 day",
            "calculation": "(Client purchase rate over 1d − Global purchase rate over 1d) / Global purchase rate over 1d, using closed='left'",
            "use_case": "Assesses short-term deviation of a client’s purchasing activity from the market baseline"
        },
        "purchase_deviation_1w": {
            "description": "Client-level purchase rate deviation from the company-wide average for the previous 1 week",
            "calculation": "(Client purchase rate over 7d − Global purchase rate over 7d) / Global purchase rate over 7d, using closed='left'",
            "use_case": "Reveals whether recent purchasing behavior is higher or lower than the global trend"
        },
        "purchase_deviation_1m": {
            "description": "Client-level purchase rate deviation from the company-wide average for the previous 1 month",
            "calculation": "(Client purchase rate over 30d − Global purchase rate over 30d) / Global purchase rate over 30d, using closed='left'",
            "use_case": "Captures medium-term patterns of customer engagement divergence from overall purchasing performance"
        },
    }

    # ========================================================================
    # 17. Detect temporary delivery issues and Potential Spamming
    # ========================================================================
    "SPAM_AND_DELIVERABILITY_FEATURES": {
        "is_soft_bounced_rate_1d": {
            "description": "Share of soft-bounced emails in the past 1 day",
            "calculation": "Rolling mean of is_soft_bounced over 1 day, closed='left'",
            "use_case": "Detect temporary delivery issues"
        },
        "is_soft_bounced_rate_1w": {
            "description": "Share of soft-bounced emails in the past 1 week",
            "calculation": "Rolling mean of is_soft_bounced over 1 week, closed='left'",
            "use_case": "Detect temporary delivery issues"
        },
        "is_soft_bounced_rate_1m": {
            "description": "Share of soft-bounced emails in the past 1 month",
            "calculation": "Rolling mean of is_soft_bounced over 1 month, closed='left'",
            "use_case": "Detect temporary delivery issues"
        },
        "is_hard_bounced_rate_1d": {
            "description": "Share of hard-bounced emails in the past day",
            "calculation": "Rolling mean of is_hard_bounced over 1 day, closed='left'",
            "use_case": "Measure list quality or spam trap risks"
        },
        "is_hard_bounced_rate_1w": {
            "description": "Share of hard-bounced emails in the past week",
            "calculation": "Rolling mean of is_hard_bounced over 7 days, closed='left'",
            "use_case": "Measure list quality or spam trap risks"
        },
        "is_hard_bounced_rate_1m": {
            "description": "Share of hard-bounced emails in the past month",
            "calculation": "Rolling mean of is_hard_bounced over 30 days, closed='left'",
            "use_case": "Measure list quality or spam trap risks"
        },
        "is_blocked_rate_1d": {
            "description": "Percentage of emails blocked by provider in the past day",
            "calculation": "Rolling mean of is_blocked over 1 days, closed='left'",
            "use_case": "Identify campaigns likely flagged as spam"
        },
        "is_blocked_rate_1w": {
            "description": "Percentage of emails blocked by provider in the past week",
            "calculation": "Rolling mean of is_blocked over 7 days, closed='left'",
            "use_case": "Identify campaigns likely flagged as spam"
        },
        "is_blocked_rate_1m": {
            "description": "Percentage of emails blocked by provider in the past month",
            "calculation": "Rolling mean of is_blocked over 30 days, closed='left'",
            "use_case": "Identify campaigns likely flagged as spam"
        },
        "is_unsubscribed_rate_1d": {
            "description": "Unsubscribe rate over the last day",
            "calculation": "Rolling mean of is_unsubscribed over 1 days, closed='left'",
            "use_case": "Detect audience fatigue or poor targeting"
        },
        "is_unsubscribed_rate_1w": {
            "description": "Unsubscribe rate over the last week",
            "calculation": "Rolling mean of is_unsubscribed over 7 days, closed='left'",
            "use_case": "Detect audience fatigue or poor targeting"
        },
        "is_unsubscribed_rate_1w": {
            "description": "Unsubscribe rate over the last month",
            "calculation": "Rolling mean of is_unsubscribed over 30 days, closed='left'",
            "use_case": "Detect audience fatigue or poor targeting"
        },
        "is_complained_rate_1d": {
            "description": "Complaint/spam report rate for the last 1 days",
            "calculation": "Rolling mean of is_complained over 1 days, closed='left'",
            "use_case": "Monitor content triggering spam complaints"
        },
        "is_complained_rate_1w": {
            "description": "Complaint/spam report rate for the last 7 days",
            "calculation": "Rolling mean of is_complained over 7 days, closed='left'",
            "use_case": "Monitor content triggering spam complaints"
        },
        "is_complained_rate_1m": {
            "description": "Complaint/spam report rate for the last 30 days",
            "calculation": "Rolling mean of is_complained over 30 days, closed='left'",
            "use_case": "Monitor content triggering spam complaints"
        },
        "spam_risk_index_1d": {
            "description": "Composite spam likelihood indicator combining bounce, block, and complaint rates",
            "calculation": "Weighted sum of bounce/block/complaint/unsubscribe metrics",
            "use_case": "Assess overall deliverability and spam reputation"
        }
        "spam_risk_index_1w": {
            "description": "Composite spam likelihood indicator combining bounce, block, and complaint rates",
            "calculation": "Weighted sum of bounce/block/complaint/unsubscribe metrics",
            "use_case": "Assess overall deliverability and spam reputation"
        }
        "spam_risk_index_1m": {
            "description": "Composite spam likelihood indicator combining bounce, block, and complaint rates",
            "calculation": "Weighted sum of bounce/block/complaint/unsubscribe metrics",
            "use_case": "Assess overall deliverability and spam reputation"
        }
    }

}


# ============================================================================
# FEATURE CATEGORIES SUMMARY
# ============================================================================

FEATURE_CATEGORIES = {
    "Temporal Features (9)": "Time-based features extracted from timestamps",
    "Channel Features (2)": "Email vs push notification indicators",
    "Campaign Type Features (4)": "Bulk, triggered, transactional indicators",
    "Rolling Volume Features (10)": "Message frequency over time windows",
    "Rolling Campaign Type Features (6)": "Campaign type exposure over time",
    "Subject Line Features (8+)": "Subject line characteristics over time",
    "Temporal Pattern Features (5)": "Weekend and working hours patterns",
    "A/B Test Features (6)": "Experimentation exposure tracking",
    "Market-Level Features (5)": "Overall market activity indicators",
    "Lagged Engagement Features (4)": "Previous message outcomes",
    "Rolling Engagement Rates (6)": "Recent engagement behavior rates",
    "Bayesian Smoothed Rates (3)": "Stable long-term engagement estimates",
    "Campaign Quality Features (6)": "Campaign-specific performance",
    "Expectation Gap Features (9)": "Behavior deviation indicators"
    "Global Company Performance Features (9)": "Overall Performace indicator"
    "Client engagement deviation (9)" : "How different the client is from the overall picture"
    "Spam and Deliverability Features (18)": "Indicate Potential Deliverability or Spamming Issues"
}


# ============================================================================
# KEY CONCEPTS
# ============================================================================

KEY_CONCEPTS = """
1. ANTI-LEAKAGE DESIGN:
   - All rolling features use closed='left' to exclude current observation
   - Engagement rates computed from shifted (_prev) values
   - Ensures features only use information available BEFORE prediction time

2. BAYESIAN SHRINKAGE:
   - Smooths rates toward global mean for clients with few observations
   - Formula: (successes + α*global_rate) / (trials + α + β)
   - Prevents overfitting to small sample sizes

3. TIME WINDOWS:
   - 1w (7 days): Recent short-term behavior
   - 1m (30 days): Medium-term patterns
   - Allows model to detect both immediate and persistent effects

4. EXPECTATION GAPS:
   - Measures deviation from baseline behavior
   - Positive gap: performing better than usual
   - Negative gap: performing worse than usual (fatigue signal)

5. MARKET-LEVEL FEATURES:
   - Captures overall platform activity
   - Helps control for time-of-day and seasonality effects
   - Merged using backward-looking merge_asof