from telethon.sync import TelegramClient
from telethon.tl.types import (
    UserStatusRecently, UserStatusLastWeek, UserStatusLastMonth,
    UserStatusOffline, UserStatusOnline
)
import csv
import json
import asyncio
import os
from datetime import datetime

# Configuration
api_id = ''
api_hash = ''
phone_number = ''
session_file = 'boss_session'

batch_size = 5000
sleep_duration = 60
csv_file = 'members.csv'

# Load group usernames
with open('group_usernames.json', 'r') as json_file:
    group_usernames = json.load(json_file)

# Initialize Telegram client
client = TelegramClient(session_file, api_id, api_hash)

# Function to extract and format user details
async def scrape_members(group_username, limit, collected_user_ids):
    await client.start(phone_number)
    group_entity = await client.get_input_entity(group_username)
    all_participants = []

    async for user in client.iter_participants(group_entity, aggressive=True):
        if user.id in collected_user_ids:
            continue

        member_data = {
            'Username': user.username or '',
            'User ID': user.id,
            'Access Hash': user.access_hash,
            'First Name': user.first_name or '',
            'Last Name': user.last_name or '',
            'Phone': user.phone or '',
            'Is Bot': user.bot,
            'Is Verified': user.verified,
            'Lang Code': user.lang_code or '',
            'Last Seen': ''
        }

        # Determine status
        if isinstance(user.status, UserStatusOnline):
            member_data['Last Seen'] = 'Online'
        elif isinstance(user.status, UserStatusOffline):
            member_data['Last Seen'] = f"Last seen at {user.status.was_online.strftime('%Y-%m-%d %H:%M:%S')}"
        elif isinstance(user.status, UserStatusRecently):
            member_data['Last Seen'] = 'Recently'
        elif isinstance(user.status, UserStatusLastWeek):
            member_data['Last Seen'] = 'Within last week'
        elif isinstance(user.status, UserStatusLastMonth):
            member_data['Last Seen'] = 'Within last month'
        else:
            member_data['Last Seen'] = 'Hidden or long ago'

        all_participants.append(member_data)
        collected_user_ids.add(user.id)

        if len(all_participants) >= limit:
            break

    return all_participants

# Save to CSV with headers
def save_members_to_csv(members):
    file_exists = os.path.exists(csv_file)
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        fieldnames = [
            'Username', 'User ID', 'Access Hash',
            'First Name', 'Last Name', 'Phone',
            'Is Bot', 'Is Verified', 'Lang Code', 'Last Seen'
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for member in members:
            writer.writerow(member)

# Main async function
async def main():
    async with client:
        for group_username in group_usernames:
            collected_user_ids = set()
            print(f"\n🔍 Scraping group: {group_username}")
            while True:
                try:
                    members = await scrape_members(group_username, batch_size, collected_user_ids)
                    if not members:
                        break
                    print(f"✅ Collected {len(members)} members.")
                    save_members_to_csv(members)
                    await asyncio.sleep(sleep_duration)
                except Exception as e:
                    print(f"⚠️ Error: {e}")
                    print(f"⏳ Retrying after {sleep_duration} seconds...")
                    await asyncio.sleep(sleep_duration)
                    continue

                if len(members) < batch_size:
                    break
            print(f"🏁 Done with group: {group_username}")

# Run the script
if __name__ == '__main__':
    asyncio.run(main())
