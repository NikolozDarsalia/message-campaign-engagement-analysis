# Dataset Documentation

This folder contains the merged dataset used for the Capstone Project on **Message Campaign Engagement Analysis**.  
It includes both **client-level** and **campaign-level** information and contains features for measuring engagement, message performance, and campaign characteristics.

## Feature Definitions

| Feature | Description |
|---------|-------------|
| `id` | Unique identifier for each message record. |
| `message_id` | Unique identifier of the individual message sent to a client. |
| `campaign_id` | Identifier of the campaign to which the message belongs. |
| `message_type` | Type of message (e.g., bulk, trigger, transactional). |
| `client_id` | Unique identifier of the recipient client. |
| `channel_x` | Channel used for sending the message from the first dataset (e.g., email, push, SMS). |
| `category` | Client/message category (e.g., marketing type or content group). |
| `platform` | Device/platform used by the client (desktop, iOS, Android). |
| `email_provider` | Email service provider of the client (e.g., Gmail, Yandex, Mail.ru). |
| `stream` | Message stream or source identifier. |
| `date` | Date (without time) when the message was sent. |
| `sent_at` | Timestamp when the message was sent. |
| `is_opened` | 1 if the message was opened, 0 otherwise. |
| `opened_first_time_at` | Timestamp of the first open by the client. |
| `opened_last_time_at` | Timestamp of the last open by the client. |
| `is_clicked` | 1 if the message link was clicked, 0 otherwise. |
| `clicked_first_time_at` | Timestamp of the first click. |
| `clicked_last_time_at` | Timestamp of the last click. |
| `is_unsubscribed` | 1 if the client unsubscribed due to the message, 0 otherwise. |
| `unsubscribed_at` | Timestamp when the client unsubscribed. |
| `is_hard_bounced` | 1 if the message experienced a permanent delivery failure, 0 otherwise. |
| `hard_bounced_at` | Timestamp of the hard bounce event. |
| `is_soft_bounced` | 1 if the message experienced a temporary delivery failure, 0 otherwise. |
| `soft_bounced_at` | Timestamp of the soft bounce event. |
| `is_complained` | 1 if the client lodged a complaint (spam report), 0 otherwise. |
| `complained_at` | Timestamp of the complaint. |
| `is_blocked` | 1 if the message was blocked by the provider, 0 otherwise. |
| `blocked_at` | Timestamp of the block event. |
| `is_purchased` | 1 if the client purchased after the message, 0 otherwise. |
| `purchased_at` | Timestamp of the purchase event. |
| `created_at` | Timestamp when the message record was created. |
| `updated_at` | Timestamp of the last update to the message record. |
| `campaign_type` | Type of the campaign (bulk, trigger, transactional). |
| `channel_y` | Channel used for the campaign from campaign dataset. |
| `topic` | Topic label for the campaign (e.g., sale, new product, event). |
| `started_at` | Timestamp when the campaign started. |
| `finished_at` | Timestamp when the campaign ended. |
| `total_count` | Number of recipients targeted in the campaign. |
| `ab_test` | 1 if the campaign was an A/B test, 0 otherwise. |
| `warmup_mode` | 1 if the campaign was sent in “warm-up” mode, 0 otherwise. |
| `hour_limit` | Max hours during which messages could be sent (bulk campaigns only). |
| `subject_length` | Number of characters in the message subject line. |
| `subject_with_personalization` | 1 if subject includes recipient personalization, 0 otherwise. |
| `subject_with_deadline` | 1 if subject includes a deadline, 0 otherwise. |
| `subject_with_emoji` | 1 if subject contains emoji, 0 otherwise. |
| `subject_with_bonuses` | 1 if subject mentions bonuses, 0 otherwise. |
| `subject_with_discount` | 1 if subject mentions a discount, 0 otherwise. |
| `subject_with_saleout` | 1 if subject mentions “sale out” or urgency, 0 otherwise. |
| `is_test` | 1 if the campaign is a test campaign, 0 otherwise. |
| `position` | Priority or position indicator for trigger campaigns. |
| `first_purchase_date` | Date of the client’s first purchase; used to measure recency and tenure. |

## Notes
- Time-based features should be aligned to the same timezone.  
- Binary flags are encoded as 0/1.  
- Features marked “bulk campaigns only” may contain nulls for other campaign types.  
- Derived features (e.g., rolling counts, recency windows) will be calculated based on these raw features for analysis and modeling.