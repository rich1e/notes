---
title: Trek 数据库表结构参考
category: references
tags:
  - database
  - persistence
  - schema
  - reference
sources:
  - "_raw/trek.txt (Gitingest export, 2026-07-02)"
created: 2026-07-02T00:00:00Z
updated: 2026-08-03T05:47:33Z
summary: Trek 使用 SQLite（better-sqlite3），所有表在 schema.ts 中初始化，核心表包括 users/trips/days/places/day_assignments，插件表在 schema 中预创建。
tier: supporting
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
base_confidence: 0.90
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.00
relationships:
  - target: "[[projects/trek/concepts/architecture-overview]]"
    type: related_to
  - target: "[[projects/trek/concepts/addon-system]]"
    type: related_to
  - target: "[[projects/trek/trek]]"
    type: related_to
---

# Trek 数据库表结构参考

Trek 使用 **SQLite**（`better-sqlite3`），数据库文件位于 `./data/travel.db`。所有表在 `server/src/db/schema.ts` 的 `createTables()` 函数中通过 `CREATE TABLE IF NOT EXISTS` 初始化，支持幂等启动。

## 核心用户表

```sql
users (id, username, email, password_hash, role,
       maps_api_key, unsplash_api_key, openweather_api_key,
       avatar, oidc_sub, oidc_issuer, last_login,
       mfa_enabled, mfa_secret, mfa_backup_codes,
       immich_url, immich_access_token,
       synology_url, synology_username, synology_password, synology_sid,
       must_change_password, password_version,
       created_at, updated_at)

password_reset_tokens (id, user_id→users, token_hash, expires_at, consumed_at, created_ip)
webauthn_credentials (id, user_id→users, credential_id, public_key, counter, 
                      transports, device_type, backed_up, name, aaguid,
                      created_at, last_used_at)
webauthn_challenges (id, challenge, user_id→users, type, expires_at)
settings (id, user_id→users, key, value)   -- 用户个人设置
app_settings (key, value)                   -- 全局应用设置（KV）
```

## 行程核心表

```sql
trips (id, user_id→users, title, description, start_date, end_date,
       currency, cover_image, is_archived, reminder_days,
       created_at, updated_at)

days (id, trip_id→trips, day_number, date, notes, title)
     UNIQUE(trip_id, day_number)

trip_members (id, trip_id→trips, user_id→users, invited_by→users, added_at)
             UNIQUE(trip_id, user_id)
```

## 地点与日程

```sql
categories (id, name, color, icon, user_id→users, created_at)
tags (id, user_id→users, name, color, created_at)

places (id, trip_id→trips, name, description, lat, lng, address,
        category_id→categories, price, currency,
        reservation_status, reservation_notes, reservation_datetime,
        place_time, end_time, duration_minutes,
        notes, image_url, google_place_id, google_ftid,
        website, phone, transport_mode,
        created_at, updated_at)

place_tags (place_id→places, tag_id→tags)  -- 多对多

day_assignments (id, day_id→days, place_id→places, order_index,
                 notes, reservation_status, reservation_notes, reservation_datetime,
                 created_at)
-- 每个地点可分配到某一天的具体时间段
```

## 预订与住宿

```sql
reservations (id, trip_id→trips, day_id→days, end_day_id→days,
              place_id→places, assignment_id→day_assignments,
              title, accommodation_id, reservation_time, reservation_end_time,
              location, confirmation_number, notes,
              status, type,         -- type: flight/hotel/restaurant/other
              created_at)

day_accommodations (id, trip_id→trips, place_id→places,
                    start_day_id→days, end_day_id→days,
                    check_in, check_in_end, check_out,
                    confirmation, notes, created_at)
```

## 预算

```sql
budget_items (id, trip_id→trips, category, name,
              total_price, persons, days, note, sort_order, created_at)
-- persons/days 用于人均/每日分摊计算
```

## 文件与照片

```sql
photos (id, trip_id→trips, day_id→days, place_id→places,
        filename, original_name, file_size, mime_type,
        caption, taken_at, created_at)

trip_files (id, trip_id→trips, place_id→places, reservation_id→reservations,
            filename, original_name, file_size, mime_type,
            description, created_at)
```

## 行李清单

```sql
packing_items (id, trip_id→trips, name, checked, category, sort_order, created_at)
```

## 日记笔记

```sql
day_notes (id, day_id→days, trip_id→trips, text, time, icon, sort_order, created_at)
-- icon: 表情符号（默认 📝）
```

## 插件表

### Vacay 插件
```sql
vacay_plans (id, owner_id→users, block_weekends, holidays_enabled, 
             holidays_region, company_holidays_enabled, carry_over_enabled)
             UNIQUE(owner_id)
vacay_plan_members (plan_id, user_id, status)
vacay_user_colors (user_id, plan_id, color)
vacay_years (plan_id, year)
vacay_user_years (user_id, plan_id, year, vacation_days, carried_over)
vacay_entries (plan_id, user_id, date, note)   UNIQUE(user_id, plan_id, date)
vacay_company_holidays (plan_id, date, note)
vacay_holiday_calendars (plan_id, region, label, color, sort_order)
```

### Collab 插件
```sql
collab_notes (id, trip_id→trips, user_id→users, category, title, content,
              color, pinned, created_at, updated_at)
collab_polls (id, trip_id→trips, user_id→users, question, ...)
-- 更多 Collab 表见 schema 后续部分
```

### Addon 系统元数据
```sql
addons (id, name, description, type, icon, enabled, config, sort_order)
photo_providers (id, name, description, icon, enabled, sort_order)
photo_provider_fields (provider_id→photo_providers, field_key, label,
                       input_type, placeholder, hint, required, secret,
                       settings_key, payload_key, sort_order)
```

## 关键设计决策

1. **外键 ON DELETE CASCADE** — 删除行程时级联删除所有相关数据（days、places、reservations 等）
2. **部分字段支持 NULL** — 如 `day_id`（未分配到具体日期的预订）、`place_id`（非地点文件）
3. **sort_order 字段** — 拖放排序的持久化依据
4. **`day_number` UNIQUE 约束** — `days` 表通过 `(trip_id, day_number)` 防止重复
5. **`password_version`** — 整型计数器，密码变更时递增，用于使旧 token 失效

## 相关页面

- [[projects/trek/concepts/architecture-overview]] — 架构概览（NestJS 模块列表）
- [[projects/trek/concepts/auth-system]] — 用户认证相关表（webauthn_credentials 等）
- [[projects/trek/concepts/addon-system]] — 插件表说明
