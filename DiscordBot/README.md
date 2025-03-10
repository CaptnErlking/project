# Pokémon Encounter & IV Logger Discord Bot

## Overview
This is a Discord bot built using `discord.py` that helps track Pokémon encounters, logs IV percentages, and provides a hunt mode for filtering Pokémon encounters based on the user's preference. The bot also allows channel locking during rare encounters and provides private notifications for certain events.

## Features
- **Pokémon Hunt Mode Selection**: Choose between two modes:
  - `Shiny Hunt (S)`: Filters out specific Pokémon encounters (Ditto, Arctozolt, Arctovish, and Dracovish).
  - `Pokemon Hunt (H)`: Displays all Pokémon encounters.
- **IV Logging**: Automatically calculates and logs Pokémon IV percentages from embedded messages.
- **Encounter Notifications**: Sends alerts for special encounters such as starter Pokémon and Greninja-Ash.
- **Channel Locking**: Temporarily locks a channel for 10 seconds when encountering rare Pokémon.
- **Private Notifications**: Sends direct messages to specified users for special conditions.
- **IV Log Management**:
  - View logged IV percentages.
  - Remove specific Pokémon from the log.
  - Clear all IV logs.

## Commands

| Command | Description |
|---------|-------------|
| `!huntmode` | Allows users to select their hunt mode using reactions. |
| `!ivlogs` | Displays all logged IV percentages. |
| `!remove_pokemon <pokemon_name>` | Removes a specific Pokémon from the IV log. |
| `!clear_ivlogs` | Clears all logged IV data. |

## Installation & Setup
### Prerequisites
- Python 3.8+
- `discord.py` installed (`pip install discord.py`)

### Running the Bot
1. Clone the repository:
   ```sh
   git clone <repo_url>
   cd <repo_directory>
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Add your bot token in `bot.run('YOUR_BOT_TOKEN')`.
4. Run the bot:
   ```sh
   python bot.py
   ```

## Usage
- The bot listens for Pokémon encounter messages and calculates IV percentages.
- Use `!huntmode` to toggle between hunting modes.
- Check logged IVs using `!ivlogs`.
- Manage IV logs using `!remove_pokemon` and `!clear_ivlogs`.

## Contributing
Feel free to fork this repository, make enhancements, and submit a pull request!

## License
This project is open-source and available under the MIT License.
