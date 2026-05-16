# Discord Review Bot for World of Warcraft

## Overview

This is a personal project built for Romanian World of Warcraft players, specifically for the guild *Dumbrava Minunată*.

The bot allows users to leave and check reviews for players based on their Raider.io profiles, helping guild members make better decisions when forming dungeon groups (especially PUGs).

It also integrates with the Raider.io API to fetch Mythic+ performance data and combine it with user-generated reviews.

---

## Features

- Submit player reviews (rating 1–10 + comment)
- View aggregated player ratings and feedback
- Automatic average rating calculation
- Private DM-based interaction for better user experience
- Input validation (rating constraints, link parsing)
- Persistent storage using MongoDB
- Raider.io API integration for character performance data

---

## How It Works

### Leave a Review

!review <raider.io link>

The bot will:
1. Send a private DM
2. Ask for a rating (1–10)
3. Ask for a short comment
4. Store the review in the database

---

### Check Reviews

!check <raider.io link>


The bot will return:
- Average rating
- All comments left by users
- Raider.io performance data

---

## Use Case

This bot is designed to help players evaluate others before inviting them into dungeon runs, especially in PUG environments where trust and performance are uncertain.

---

## Tech Stack

- Python
- discord.py
- MongoDB
- Requests (API handling)
- Asyncio
- Raider.io API

---

## Future Improvements

- Leaderboard system
- Edit/delete reviews
- Role-based analytics improvements
- Web dashboard

---

## What I Learned

- Asynchronous programming in Python (async/await)
- Working with REST APIs (Raider.io)
- Handling MongoDB data storage
- Building interactive Discord bots
- Designing user interaction flows
- Combining external APIs with user-generated data
