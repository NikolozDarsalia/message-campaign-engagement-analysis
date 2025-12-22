# Feature Engineering Documentation

This document describes all features created through feature engineering for email/push message campaign analysis.

---

## Table of Contents

1. [Temporal Features](#1-temporal-features)
2. [Channel Features](#2-channel-features)
3. [Campaign Type Features](#3-campaign-type-features)
4. [Rolling Message Volume Features](#4-rolling-message-volume-features)
5. [Rolling Campaign Type Features](#5-rolling-campaign-type-features)
6. [Subject Line Features](#6-subject-line-features-rolling)
7. [Temporal Pattern Features](#7-temporal-pattern-features-rolling)
8. [A/B Test and Warm-up Features](#8-ab-test-and-warm-up-features)
9. [Market-Level Features](#9-market-level-features)
10. [Lagged Engagement Features](#10-lagged-engagement-features-anti-leakage)
11. [Rolling Engagement Rates](#11-rolling-engagement-rates-anti-leakage)
12. [Bayesian Smoothed Rates](#12-bayesian-smoothed-rates-anti-leakage)
13. [Campaign-Level Quality Features](#13-campaign-level-quality-features)
14. [Customer Expectation Gap Features](#14-customer-expectation-gap-features)
15. [Global Company Performance Features](#15-global-company-performance-features)
16. [Client Engagement Deviation Features](#16-client-engagement-deviation-features)
17. [Spam and Deliverability Features](#17-spam-and-deliverability-features)
18. [Time Since Last Action Features](#18-time-since-last-action-features)
19. [Rolling Time-to-Action Features](#19-rolling-time-to-action-features)
20. [Open/Click Count Window Features](#20-openclick-count-window-features)
21. [Prior Precision Features](#21-prior-precision-features-open-rate-stability)
22. [Holiday Distance Features](#22-holiday-distance-features)

---

## 1. Temporal Features

Basic time-based features extracted from timestamps.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `hour` | Hour of day when message was sent (0-23) | Extracted from sent_at timestamp | Identify optimal send times |
| `weekday` | Day of week (0=Monday, 6=Sunday) | Extracted from sent_at timestamp | Understand weekly patterns |
| `is_weekend` | Binary indicator if message sent on weekend | 1 if weekday >= 5, else 0 | Weekend vs weekday performance comparison |
| `is_working_hours` | Binary indicator if sent during working hours (9-18) | 1 if hour between 9 and 18, else 0 | Business hours engagement patterns |
| `days_since_last_msg` | Days elapsed since previous message to same client | Difference between current and previous sent_at per client | Measure message frequency and fatigue |
| `days_since_last_email` | Days since last email to this client | Time difference for email channel only | Email-specific frequency analysis |
| `days_since_last_push` | Days since last push notification to this client | Time difference for push channel only | Push notification frequency analysis |
| `time_to_open_hours` | Hours between send and first open | (opened_first_time_at - sent_at) in hours | Measure engagement speed |
| `time_to_click_hours` | Hours between send and first click | (clicked_first_time_at - sent_at) in hours | Measure conversion speed |
| `days_since_last_bulk` | Days since last bulk to this client | Time difference for bulk campaigns only | Campaign-specific frequency analysis |
| `days_since_last_trigger` | Days since last trigger to this client | Time difference for trigger campaigns only | Campaign-specific frequency analysis |
| `days_since_last_transactional` | Days since last transactional to this client | Time difference for transactional campaigns only | Campaign-specific frequency analysis |

---

## 2. Channel Features

Binary indicators for communication channels.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `is_email` | Binary indicator for email channel | 1 if channel_x == 'email', else 0 | Channel-specific modeling |
| `is_push` | Binary indicator for push notification | 1 if channel_x == 'push', else 0 | Channel-specific modeling |

---

## 3. Campaign Type Features

Features identifying campaign types and message position.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `is_bulk` | Binary indicator for bulk campaign | 1 if campaign_type == 'bulk', else 0 | Mass marketing campaign identification |
| `is_triggered` | Binary indicator for triggered campaign | 1 if campaign_type == 'triggered', else 0 | Behavioral trigger campaign identification |
| `is_transactional` | Binary indicator for transactional message | 1 if campaign_type == 'transactional', else 0 | Transaction-related message identification |
| `msg_position_in_campaign` | Sequential position of message within campaign for client | Cumulative count within (client_id, campaign_id) group | Track message series progression |

---

## 4. Rolling Message Volume Features

Message frequency metrics over various time windows.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `sent_count_1d` | Number of messages sent to client in past 1 day | Rolling count over 1d window, closed='left' (excludes current) | Recent message frequency, fatigue detection |
| `sent_count_1w` | Number of messages sent to client in past 7 days | Rolling count over 7d window, closed='left' | Recent message frequency, fatigue detection |
| `sent_count_1m` | Number of messages sent to client in past 30 days | Rolling count over 30d window, closed='left' | Monthly message frequency |
| `sent_count_email_1d` | Email messages to client in past day | Rolling sum of is_email over 1d, closed='left' | Email-specific frequency |
| `sent_count_email_1w` | Email messages to client in past week | Rolling sum of is_email over 7d, closed='left' | Email-specific frequency |
| `sent_count_email_1m` | Email messages to client in past month | Rolling sum of is_email over 30d, closed='left' | Monthly email frequency |
| `sent_count_push_1d` | Push notifications to client in past day | Rolling sum of is_push over 1d, closed='left' | Push notification frequency |
| `sent_count_push_1w` | Push notifications to client in past week | Rolling sum of is_push over 7d, closed='left' | Push notification frequency |
| `sent_count_push_1m` | Push notifications to client in past month | Rolling sum of is_push over 30d, closed='left' | Monthly push frequency |
| `avg_interval_1d` | Average days between messages in past day | Rolling mean of days_since_last_msg over 1d, closed='left' | Message pacing consistency |
| `avg_interval_1w` | Average days between messages in past week | Rolling mean of days_since_last_msg over 7d, closed='left' | Message pacing consistency |
| `avg_interval_1m` | Average days between messages in past month | Rolling mean of days_since_last_msg over 30d, closed='left' | Long-term message pacing |
| `unique_campaigns_1d` | Number of distinct campaigns client received in past day | Rolling nunique of campaign_id over 1d, closed='left' | Campaign diversity exposure |
| `unique_campaigns_1w` | Number of distinct campaigns client received in past week | Rolling nunique of campaign_id over 7d, closed='left' | Campaign diversity exposure |
| `unique_campaigns_1m` | Number of distinct campaigns client received in past month | Rolling nunique of campaign_id over 30d, closed='left' | Monthly campaign variety |

---

## 5. Rolling Campaign Type Features

Campaign type exposure over time windows.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `bulk_count_1d` | Bulk campaigns received in past day | Rolling sum of is_bulk over 1d, closed='left' | Bulk campaign exposure |
| `bulk_count_1w` | Bulk campaigns received in past week | Rolling sum of is_bulk over 7d, closed='left' | Bulk campaign exposure |
| `bulk_count_1m` | Bulk campaigns received in past month | Rolling sum of is_bulk over 30d, closed='left' | Monthly bulk exposure |
| `triggered_count_1d` | Triggered campaigns received in past day | Rolling sum of is_triggered over 1d, closed='left' | Behavioral trigger exposure |
| `triggered_count_1w` | Triggered campaigns received in past week | Rolling sum of is_triggered over 7d, closed='left' | Behavioral trigger exposure |
| `triggered_count_1m` | Triggered campaigns received in past month | Rolling sum of is_triggered over 30d, closed='left' | Monthly triggered exposure |
| `transactional_count_1d` | Transactional messages received in past day | Rolling sum of is_transactional over 1d, closed='left' | Transaction message frequency |
| `transactional_count_1w` | Transactional messages received in past week | Rolling sum of is_transactional over 7d, closed='left' | Transaction message frequency |
| `transactional_count_1m` | Transactional messages received in past month | Rolling sum of is_transactional over 30d, closed='left' | Monthly transaction messages |

---

## 6. Subject Line Features (Rolling)

Subject line characteristics aggregated over time windows.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `avg_subject_len_1d` | Average subject line length in past day | Rolling mean of subject_length over 1d, closed='left' | Subject length consistency |
| `avg_subject_len_1w` | Average subject line length in past week | Rolling mean of subject_length over 7d, closed='left' | Subject length consistency |
| `avg_subject_len_1m` | Average subject line length in past month | Rolling mean of subject_length over 30d, closed='left' | Long-term subject length patterns |
| `subject_personalization_prop_1d` | Proportion of subjects with personalization in past day | Rolling mean of subject_with_personalization over 1d | Personalization exposure |
| `subject_personalization_prop_1w` | Proportion of subjects with personalization in past week | Rolling mean of subject_with_personalization over 7d | Personalization exposure |
| `subject_personalization_prop_1m` | Proportion of subjects with personalization in past month | Rolling mean of subject_with_personalization over 30d | Monthly personalization rate |
| `subject_bonuses_prop_1d` | Proportion of subjects mentioning bonuses in past day | Rolling mean of subject_with_bonuses over 1d | Bonus offer frequency |
| `subject_bonuses_prop_1w` | Proportion of subjects mentioning bonuses in past week | Rolling mean of subject_with_bonuses over 7d | Bonus offer frequency |
| `subject_bonuses_prop_1m` | Proportion of subjects mentioning bonuses in past month | Rolling mean of subject_with_bonuses over 30d | Bonus offer frequency |
| `subject_discount_prop_1d` | Proportion of subjects with discount mentions in past day | Rolling mean of subject_with_discount over 1d | Discount promotion exposure |
| `subject_discount_prop_1w` | Proportion of subjects with discount mentions in past week | Rolling mean of subject_with_discount over 7d | Discount promotion exposure |
| `subject_discount_prop_1m` | Proportion of subjects with discount mentions in past month | Rolling mean of subject_with_discount over 30d | Discount promotion exposure |
| `subject_deadline_prop_1d` | Proportion of subjects with urgency/deadline in past day | Rolling mean of subject_with_deadline over 1d | Urgency tactic frequency |
| `subject_deadline_prop_1w` | Proportion of subjects with urgency/deadline in past week | Rolling mean of subject_with_deadline over 7d | Urgency tactic frequency |
| `subject_deadline_prop_1m` | Proportion of subjects with urgency/deadline in past month | Rolling mean of subject_with_deadline over 30d | Urgency tactic frequency |
| `subject_emoji_prop_1d` | Proportion of subjects with emoji in past day | Rolling mean of subject_with_emoji over 1d | Emoji usage patterns |
| `subject_emoji_prop_1w` | Proportion of subjects with emoji in past week | Rolling mean of subject_with_emoji over 7d | Emoji usage patterns |
| `subject_emoji_prop_1m` | Proportion of subjects with emoji in past month | Rolling mean of subject_with_emoji over 30d | Emoji usage patterns |

---

## 7. Temporal Pattern Features (Rolling)

Time-based sending patterns.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `weekend_ratio_1w` | Proportion of messages sent on weekends in past week | Rolling mean of is_weekend over 7d, closed='left' | Weekend sending patterns |
| `weekend_ratio_1m` | Proportion of messages sent on weekends in past month | Rolling mean of is_weekend over 30d, closed='left' | Monthly weekend patterns |
| `working_hours_ratio_1d` | Proportion sent during working hours in past day | Rolling mean of is_working_hours over 1d, closed='left' | Business hours sending patterns |
| `working_hours_ratio_1w` | Proportion sent during working hours in past week | Rolling mean of is_working_hours over 7d, closed='left' | Business hours sending patterns |
| `working_hours_ratio_1m` | Proportion sent during working hours in past month | Rolling mean of is_working_hours over 30d, closed='left' | Monthly business hours patterns |

---

## 8. A/B Test and Warm-up Features

Experimentation and warm-up phase tracking.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `ab_test_count_1d` | Number of A/B test messages in past day | Rolling sum of ab_test over 1d, closed='left' | A/B test exposure tracking |
| `ab_test_count_1w` | Number of A/B test messages in past week | Rolling sum of ab_test over 7d, closed='left' | A/B test exposure tracking |
| `ab_test_count_1m` | Number of A/B test messages in past month | Rolling sum of ab_test over 30d, closed='left' | Monthly A/B test frequency |
| `warmup_mode_count_1d` | Number of warm-up mode messages in past day | Rolling sum of warmup_mode over 1d, closed='left' | Warm-up phase tracking |
| `warmup_mode_count_1w` | Number of warm-up mode messages in past week | Rolling sum of warmup_mode over 7d, closed='left' | Warm-up phase tracking |
| `warmup_mode_count_1m` | Number of warm-up mode messages in past month | Rolling sum of warmup_mode over 30d, closed='left' | Monthly warm-up exposure |

---

## 9. Market-Level Features

Platform-wide activity indicators.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `total_msgs` | Total messages sent across all clients in current hour | Count of messages per hour bucket | Market-level activity indicator |
| `market_avg_msgs_6h` | Average hourly messages in past 6 hours (market-wide) | Rolling mean of total_msgs over 6H, closed='left' | Short-term market activity |
| `market_avg_msgs_1d` | Average hourly messages in past day (market-wide) | Rolling mean of total_msgs over 1D, closed='left' | Daily market activity |
| `market_avg_msgs_1w` | Average hourly messages in past week (market-wide) | Rolling mean of total_msgs over 7D, closed='left' | Weekly market trends |
| `market_avg_msgs_1m` | Average hourly messages in past month (market-wide) | Rolling mean of total_msgs over 30D, closed='left' | Long-term market baseline |

---

## 10. Lagged Engagement Features (Anti-Leakage)

Previous message outcomes to prevent data leakage.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `is_opened_prev` | Whether previous message was opened | Shifted is_opened by 1 position per client | Previous engagement indicator, prevents leakage |
| `is_clicked_prev` | Whether previous message was clicked | Shifted is_clicked by 1 position per client | Previous click behavior |
| `is_purchased_prev` | Whether previous message led to purchase | Shifted is_purchased by 1 position per client | Previous conversion indicator |
| `time_to_open_hours_prev` | Hours to open for previous message | Shifted time_to_open_hours by 1 position per client | Previous engagement speed |
| `time_to_click_hours_prev` | Hours to click for previous message | Shifted time_to_click_hours by 1 position per client | Previous conversion speed |

---

## 11. Rolling Engagement Rates (Anti-Leakage)

Recent engagement behavior without data leakage.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `is_opened_rate_1w` | Open rate over past week (excluding current message) | Rolling mean of is_opened_prev over 7d, closed='left' | Recent open behavior, no leakage |
| `is_opened_rate_1m` | Open rate over past month (excluding current message) | Rolling mean of is_opened_prev over 30d, closed='left' | Long-term open behavior |
| `is_clicked_rate_1w` | Click rate over past week (excluding current message) | Rolling mean of is_clicked_prev over 7d, closed='left' | Recent click behavior |
| `is_clicked_rate_1m` | Click rate over past month (excluding current message) | Rolling mean of is_clicked_prev over 30d, closed='left' | Long-term click behavior |
| `is_purchased_rate_1w` | Purchase rate over past week (excluding current message) | Rolling mean of is_purchased_prev over 7d, closed='left' | Recent conversion behavior |
| `is_purchased_rate_1m` | Purchase rate over past month (excluding current message) | Rolling mean of is_purchased_prev over 30d, closed='left' | Long-term conversion behavior |

---

## 12. Bayesian Smoothed Rates (Anti-Leakage)

Stable long-term engagement estimates using Bayesian shrinkage.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `is_opened_rate_prev_smooth` | Smoothed historical open rate (Bayesian shrinkage) | (cumsum_prev + α×global_rate) / (trials + α + β) | Stable open rate estimate, handles low counts |
| `is_clicked_rate_prev_smooth` | Smoothed historical click rate (Bayesian shrinkage) | (cumsum_prev + α×global_rate) / (trials + α + β) | Stable click rate estimate, handles low counts |
| `is_purchased_rate_prev_smooth` | Smoothed historical purchase rate (Bayesian shrinkage) | (cumsum_prev + α×global_rate) / (trials + α + β) | Stable conversion rate estimate, handles low counts |

---

## 13. Campaign-Level Quality Features

Campaign-specific performance metrics.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `is_opened_rate_campaign_per_client` | Historical open rate for this campaign (for this client) | Expanding mean of is_opened shifted by 1, per (client, campaign) | Campaign-specific open performance |
| `is_clicked_rate_campaign_per_client` | Historical click rate for this campaign (for this client) | Expanding mean of is_clicked shifted by 1, per (client, campaign) | Campaign-specific click performance |
| `is_purchased_rate_campaign_per_client` | Historical purchase rate for this campaign (for this client) | Expanding mean of is_purchased shifted by 1, per (client, campaign) | Campaign-specific conversion performance |
| `is_opened_rate_campaign` | Historical open rate for this campaign | Expanding mean of is_opened shifted by 1, per campaign | Campaign-specific open performance |
| `is_clicked_rate_campaign` | Historical click rate for this campaign | Expanding mean of is_clicked shifted by 1, per campaign | Campaign-specific click performance |
| `is_purchased_rate_campaign` | Historical purchase rate for this campaign | Expanding mean of is_purchased shifted by 1, per campaign | Campaign-specific conversion performance |

---

## 14. Customer Expectation Gap Features

Deviation from baseline behavior indicating fatigue or revival.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `is_opened_expect_gap_1w` | Gap between recent (1w) and long-term open behavior | is_opened_rate_1w - is_opened_rate_prev_smooth | Detect recent behavior changes (fatigue/revival) |
| `is_opened_expect_gap_1m` | Gap between recent (1m) and long-term open behavior | is_opened_rate_1m - is_opened_rate_prev_smooth | Monthly behavior deviation |
| `is_opened_expect_gap_overall` | Gap between overall average and smoothed open rate | client_avg_is_opened - is_opened_rate_prev_smooth | Overall engagement vs baseline |
| `is_clicked_expect_gap_1w` | Gap between recent (1w) and long-term click behavior | is_clicked_rate_1w - is_clicked_rate_prev_smooth | Recent click behavior change |
| `is_clicked_expect_gap_1m` | Gap between recent (1m) and long-term click behavior | is_clicked_rate_1m - is_clicked_rate_prev_smooth | Monthly click behavior deviation |
| `is_clicked_expect_gap_overall` | Gap between overall average and smoothed click rate | client_avg_is_clicked - is_clicked_rate_prev_smooth | Overall click engagement vs baseline |
| `is_purchased_expect_gap_1w` | Gap between recent (1w) and long-term purchase behavior | is_purchased_rate_1w - is_purchased_rate_prev_smooth | Recent conversion change |
| `is_purchased_expect_gap_1m` | Gap between recent (1m) and long-term purchase behavior | is_purchased_rate_1m - is_purchased_rate_prev_smooth | Monthly conversion deviation |
| `is_purchased_expect_gap_overall` | Gap between overall average and smoothed purchase rate | client_avg_is_purchased - is_purchased_rate_prev_smooth | Overall conversion vs baseline |

---

## 15. Global Company Performance Features

Company-wide engagement metrics over time.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `global_is_opened_rate_1d` | Open rate for the last 1 day | Rolling mean of is_opened over 1d, closed='left' | Detect customers relationship to the company for the recent period |
| `global_is_opened_rate_1w` | Open rate for the last 1 week | Rolling mean of is_opened over 1w, closed='left' | Detect customers relationship to the company for the recent period |
| `global_is_opened_rate_1m` | Open rate for the last 1 month | Rolling mean of is_opened over 1m, closed='left' | Detect customers relationship to the company for the recent period |
| `global_is_clicked_rate_1d` | Click rate for the last 1 day | Rolling mean of is_clicked over 1d, closed='left' | Detect customers relationship to the company for the recent period |
| `global_is_clicked_rate_1w` | Click rate for the last 1 week | Rolling mean of is_clicked over 1w, closed='left' | Detect customers relationship to the company for the recent period |
| `global_is_clicked_rate_1m` | Click rate for the last 1 month | Rolling mean of is_clicked over 1m, closed='left' | Detect customers relationship to the company for the recent period |
| `global_is_purchased_rate_1d` | Purchase rate for the last 1 day | Rolling mean of is_purchased over 1d, closed='left' | Detect customers relationship to the company for the recent period |
| `global_is_purchased_rate_1w` | Purchase rate for the last 1 week | Rolling mean of is_purchased over 1w, closed='left' | Detect customers relationship to the company for the recent period |
| `global_is_purchased_rate_1m` | Purchase rate for the last 1 month | Rolling mean of is_purchased over 1m, closed='left' | Detect customers relationship to the company for the recent period |

---

## 16. Client Engagement Deviation Features

How individual client engagement differs from company-wide averages.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `open_deviation_1d` | Client-level open rate deviation from company-wide average for previous 1 day | (Client open rate over 1d − Global open rate over 1d) / Global open rate over 1d, closed='left' | Measures how much more or less engaged a client is compared to average over past day |
| `open_deviation_1w` | Client-level open rate deviation from company-wide average for previous 1 week | (Client open rate over 7d − Global open rate over 7d) / Global open rate over 7d, closed='left' | Identifies short-term engagement divergence compared to global trends |
| `open_deviation_1m` | Client-level open rate deviation from company-wide average for previous 1 month | (Client open rate over 30d − Global open rate over 30d) / Global open rate over 30d, closed='left' | Captures medium-term engagement divergence |
| `click_deviation_1d` | Client-level click rate deviation from company-wide average for previous 1 day | (Client click rate over 1d − Global click rate over 1d) / Global click rate over 1d, closed='left' | Detects how client's short-term click activity differs from global behavior |
| `click_deviation_1w` | Client-level click rate deviation from company-wide average for previous 1 week | (Client click rate over 7d − Global click rate over 7d) / Global click rate over 7d, closed='left' | Highlights short-term differences in engagement patterns |
| `click_deviation_1m` | Client-level click rate deviation from company-wide average for previous 1 month | (Client click rate over 30d − Global click rate over 30d) / Global click rate over 30d, closed='left' | Evaluates whether client's click trend aligns with overall market |
| `purchase_deviation_1d` | Client-level purchase rate deviation from company-wide average for previous 1 day | (Client purchase rate over 1d − Global purchase rate over 1d) / Global purchase rate over 1d, closed='left' | Assesses short-term deviation of purchasing activity from baseline |
| `purchase_deviation_1w` | Client-level purchase rate deviation from company-wide average for previous 1 week | (Client purchase rate over 7d − Global purchase rate over 7d) / Global purchase rate over 7d, closed='left' | Reveals whether recent purchasing is higher or lower than global trend |
| `purchase_deviation_1m` | Client-level purchase rate deviation from company-wide average for previous 1 month | (Client purchase rate over 30d − Global purchase rate over 30d) / Global purchase rate over 30d, closed='left' | Captures medium-term patterns of customer engagement divergence |

---

## 17. Spam and Deliverability Features

Indicators of potential deliverability issues and spam behavior.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `is_soft_bounced_rate_1d` | Share of soft-bounced emails in the past 1 day | Rolling mean of is_soft_bounced over 1 day, closed='left' | Detect temporary delivery issues |
| `is_soft_bounced_rate_1w` | Share of soft-bounced emails in the past 1 week | Rolling mean of is_soft_bounced over 1 week, closed='left' | Detect temporary delivery issues |
| `is_soft_bounced_rate_1m` | Share of soft-bounced emails in the past 1 month | Rolling mean of is_soft_bounced over 1 month, closed='left' | Detect temporary delivery issues |
| `is_hard_bounced_rate_1d` | Share of hard-bounced emails in the past day | Rolling mean of is_hard_bounced over 1 day, closed='left' | Measure list quality or spam trap risks |
| `is_hard_bounced_rate_1w` | Share of hard-bounced emails in the past week | Rolling mean of is_hard_bounced over 7 days, closed='left' | Measure list quality or spam trap risks |
| `is_hard_bounced_rate_1m` | Share of hard-bounced emails in the past month | Rolling mean of is_hard_bounced over 30 days, closed='left' | Measure list quality or spam trap risks |
| `is_blocked_rate_1d` | Percentage of emails blocked by provider in the past day | Rolling mean of is_blocked over 1 day, closed='left' | Identify campaigns likely flagged as spam |
| `is_blocked_rate_1w` | Percentage of emails blocked by provider in the past week | Rolling mean of is_blocked over 7 days, closed='left' | Identify campaigns likely flagged as spam |
| `is_blocked_rate_1m` | Percentage of emails blocked by provider in the past month | Rolling mean of is_blocked over 30 days, closed='left' | Identify campaigns likely flagged as spam |
| `is_unsubscribed_rate_1d` | Unsubscribe rate over the last day | Rolling mean of is_unsubscribed over 1 day, closed='left' | Detect audience fatigue or poor targeting |
| `is_unsubscribed_rate_1w` | Unsubscribe rate over the last week | Rolling mean of is_unsubscribed over 7 days, closed='left' | Detect audience fatigue or poor targeting |
| `is_unsubscribed_rate_1m` | Unsubscribe rate over the last month | Rolling mean of is_unsubscribed over 30 days, closed='left' | Detect audience fatigue or poor targeting |
| `is_complained_rate_1d` | Complaint/spam report rate for the last 1 day | Rolling mean of is_complained over 1 day, closed='left' | Monitor content triggering spam complaints |
| `is_complained_rate_1w` | Complaint/spam report rate for the last 7 days | Rolling mean of is_complained over 7 days, closed='left' | Monitor content triggering spam complaints |
| `is_complained_rate_1m` | Complaint/spam report rate for the last 30 days | Rolling mean of is_complained over 30 days, closed='left' | Monitor content triggering spam complaints |
| `spam_risk_index_1d` | Composite spam likelihood indicator (1 day) | Weighted sum of bounce/block/complaint/unsubscribe metrics | Assess overall deliverability and spam reputation |
| `spam_risk_index_1w` | Composite spam likelihood indicator (1 week) | Weighted sum of bounce/block/complaint/unsubscribe metrics | Assess overall deliverability and spam reputation |
| `spam_risk_index_1m` | Composite spam likelihood indicator (1 month) | Weighted sum of bounce/block/complaint/unsubscribe metrics | Assess overall deliverability and spam reputation |

---

## 18. Time Since Last Action Features

Recency of client engagement actions.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `time_since_last_open_hours` | Hours since the client last opened any previous message | Time difference in hours between sent_at and previous message with is_opened==1, per client | Captures recency of engagement and potential freshness of attention |
| `time_since_last_click_hours` | Hours since the client last clicked any previous message | Time difference in hours between sent_at and previous message with is_clicked==1, per client | Measures recency of deeper engagement or interest |
| `time_since_last_purchase_hours` | Hours since the client last made a purchase attributed to any previous message | Time difference in hours between sent_at and previous message with is_purchased==1, per client | Proxy for time since last economic transaction, relevant for propensity to respond |

---

## 19. Rolling Time-to-Action Features

Average reaction speed metrics over time windows.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `time_to_open_hours_avg_1m` | Average time to open in the past month (excluding current message) | Rolling mean of time_to_open_hours over 30d window per client, closed='left' | Captures how quickly the client typically reacts to messages in recent history |
| `time_to_click_hours_avg_1m` | Average time to click in the past month (excluding current message) | Rolling mean of time_to_click_hours over 30d window per client, closed='left' | Measures recent speed of deeper engagement and conversion |

---

## 20. Open/Click Count Window Features

Short- and medium-term engagement volume metrics.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `opened_count_1w` | Number of messages opened by the client in the past week | Rolling sum of is_opened over 7d window per client, closed='left' (excludes current) | Short-term intensity of engagement with messages |
| `opened_count_1m` | Number of messages opened by the client in the past month | Rolling sum of is_opened over 30d window per client, closed='left' | Medium-term engagement volume |
| `opened_count_1m_ex_1w` | Number of messages opened in the past month excluding the last week | opened_count_1m − opened_count_1w | Separates older engagement from recent engagement to detect slowdowns |
| `clicked_count_1w` | Number of messages clicked by the client in the past week | Rolling sum of is_clicked over 7d window per client, closed='left' | Short-term depth of engagement |
| `clicked_count_1m` | Number of messages clicked by the client in the past month | Rolling sum of is_clicked over 30d window per client, closed='left' | Medium-term depth of engagement |
| `clicked_count_1m_ex_1w` | Number of messages clicked in the past month excluding the last week | clicked_count_1m − clicked_count_1w | Highlights whether clicks are concentrated recently or in earlier weeks |

---

## 21. Prior Precision Features (Open Rate Stability)

Measures stability of client engagement behavior.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `open_rate_14d_prior_var` | Variance of past non-overlapping 14-day open rates for the client before the current message | For each client and message at time t, partition history into consecutive 14d windows strictly before t; compute open rate in each window with at least one message; take variance across window open rates, returning NaN if fewer than 2 windows exist | Measures stability of client's historical open behavior; lower variance implies higher prior precision over engagement propensity |

---

## 22. Holiday Distance Features

Temporal distance to major holidays.

| Feature | Description | Calculation | Use Case |
|---------|-------------|-------------|----------|
| `days_since_last_holiday` | Days since the most recent holiday date before the message was sent | Using holiday calendar, merge_asof with direction='backward' (strictly < sent_at) to find last holiday and compute (sent_at − last_holiday_date) in days | Captures post-holiday effects on attention and shopping behavior |
| `days_until_next_holiday` | Days until the next upcoming holiday date after the message was sent | Using holiday calendar, merge_asof with direction='forward' (strictly > sent_at) to find next holiday and compute (next_holiday_date − sent_at) in days | Captures pre-holiday buildup and increased relevance of promotional messages |

---

## Feature Categories Summary

| Category | Description | Count |
|----------|-------------|-------|
| Temporal Features | Time-based features extracted from timestamps | 12 |
| Channel Features | Email vs push notification indicators | 2 |
| Campaign Type Features | Bulk, triggered, transactional indicators | 4 |
| Rolling Volume Features | Message frequency over time windows | 10 |
| Rolling Campaign Type Features | Campaign type exposure over time | 6 |
| Subject Line Features | Subject line characteristics over time | 8+ |
| Temporal Pattern Features | Weekend and working hours patterns | 5 |
| A/B Test Features | Experimentation exposure tracking | 6 |
| Market-Level Features | Overall market activity indicators | 5 |
| Lagged Engagement Features | Previous message outcomes | 4 |
| Rolling Engagement Rates | Recent engagement behavior rates | 6 |
| Bayesian Smoothed Rates | Stable long-term engagement estimates | 3 |
| Campaign Quality Features | Campaign-specific performance | 6 |
| Expectation Gap Features | Behavior deviation indicators | 9 |
| Global Company Performance Features | Overall performance indicator | 9 |
| Client Engagement Deviation | How different the client is from the overall picture | 9 |
| Spam and Deliverability Features | Indicate potential deliverability or spamming issues | 18 |
| Time Since Last Action Features | Recency of opens, clicks, and purchases | 3 |
| Rolling Time-to-Action Features | Recent average reaction speed | 2 |
| Open/Click Count Window Features | Short- and medium-term engagement volumes | 6 |
| Prior Precision Features | Stability of client open behavior over 14-day blocks | 1 |
| Holiday Distance Features | Time to and from major holidays | 2 |

---

## Key Concepts

### 1. Anti-Leakage Design

All rolling features use `closed='left'` to exclude the current observation, ensuring features only use information available **before** prediction time:

- Engagement rates are computed from shifted (`_prev`) values
- Rolling windows exclude the current message
- Prevents data leakage that would artificially inflate model performance

### 2. Bayesian Shrinkage

Smooths rates toward the global mean for clients with few observations:

**Formula:** `(successes + α × global_rate) / (trials + α + β)`

This approach:
- Prevents overfitting to small sample sizes
- Provides more stable estimates for new or low-activity clients
- Gradually converges to the empirical rate as more data accumulates

### 3. Time Windows

Different time windows capture various behavioral patterns:

- **1d (1 day):** Very recent, immediate behavior
- **1w (7 days):** Recent short-term behavior
- **1m (30 days):** Medium-term patterns

This allows the model to detect both immediate reactions and persistent long-term effects.

### 4. Expectation Gaps

Measures deviation from baseline behavior to detect engagement changes:

- **Positive gap:** Client is performing better than their usual baseline (revival, high interest)
- **Negative gap:** Client is performing worse than usual (fatigue signal, declining interest)
- **Near-zero gap:** Behavior is consistent with historical patterns

These features are powerful for detecting when clients are becoming disengaged or re-engaging.

### 5. Market-Level Features

Captures overall platform activity to control for external factors:

- Reflects time-of-day effects (peak vs off-peak hours)
- Captures seasonality and market-wide trends
- Merged using backward-looking `merge_asof` to prevent leakage
- Helps distinguish client-specific behavior from market-wide patterns

---

## Implementation Notes

### Feature Engineering Pipeline

1. **Sort data** by `client_id` and `sent_at` timestamp
2. **Create base features** (temporal, channel, campaign type)
3. **Compute rolling windows** with `closed='left'`
4. **Shift engagement outcomes** to create lagged features
5. **Calculate rates and aggregations** from lagged values
6. **Merge market-level features** using `merge_asof`
7. **Compute expectation gaps** as differences between rates

### Performance Considerations

- Use efficient pandas operations (`rolling`, `shift`, `groupby`)
- Pre-sort dataframes for optimal performance
- Consider memory usage with large rolling windows
- Cache intermediate results when possible

### Data Quality

- Handle missing values appropriately (NaN for insufficient history)
- Validate that rolling windows contain enough data points
- Check for data leakage in validation sets
- Ensure temporal ordering is preserved throughout pipeline