from environs import Env



env = Env()
env.read_env()



BOT_TOKEN = env.str("BOT_TOKEN")  # bot tokeni

ADMINS_ = env.list("ADMINS")  # admin id raqamlari
ADMINS = [int(admin) for admin in ADMINS_]




CHANNELS_ = env.list("CHANNELS")  # kanal id raqamlari
CHANNELS = [int(channel) for channel in CHANNELS_]

CHANNEL_LINK = env.str("CHANNEL_LINK") # kanal linki

ADMIN_GROUP = env.int("ADMIN_GROUP") # admin guruhi



