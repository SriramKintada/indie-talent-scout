"""
Domain registries, geographic hubs, and prompt templates for Indian creative scouting.
"""

MUSIC_DOMAINS = [
    "bandcamp.com",
    "soundcloud.com",
    "open.spotify.com",
    "homegrown.co.in",
    "thewildcity.com",
    "rollingstoneindia.com",
    "youtube.com",
]

DESIGN_DOMAINS = [
    "behance.net",
    "bento.me",
    "readcv.com",
    "layers.to",
    "neocities.org",
    "homegrown.co.in",
    "platform-mag.com",
]

ALL_DOMAINS = [
    "bandcamp.com",
    "soundcloud.com",
    "behance.net",
    "bento.me",
    "readcv.com",
    "neocities.org",
    "homegrown.co.in",
]

INDIAN_SCENE_HUBS = {
    "delhi": "Delhi-NCR, Gurgaon, Hauz Khas, Shahpur Jat",
    "bangalore": "Bangalore, Bengaluru, Indiranagar, Koramangala",
    "kerala": "Kerala, Kochi, Calicut, Trivandrum",
    "northeast": "Shillong, Imphal, Guwahati, Kohima, Nagaland, Meghalaya",
    "mumbai": "Mumbai, Bandra, Pune",
    "kolkata": "Kolkata, Salt Lake",
    "goa": "Goa, Anjuna, Panjim",
    "india": "India",
}

ROLE_TEMPLATES = {
    "music": (
        "Here is an independent indie singer, music producer, or songwriter from {region} "
        "making {vibe} music on Bandcamp, SoundCloud, or Spotify:"
    ),
    "singer": (
        "Here is an independent indie singer-songwriter from {region} "
        "singing soulful {vibe} songs with acoustic guitar or piano:"
    ),
    "producer": (
        "Here is an independent electronic music producer or beatmaker from {region} "
        "releasing {vibe} soundscapes or tracks:"
    ),
    "sound": (
        "Here is an independent audio designer or sonic artist based in {region} "
        "creating {vibe} sound design, earcons, or ambient music:"
    ),
    "design": (
        "Here is the portfolio of an independent graphic designer, visual illustrator, or UI craftsman "
        "based in {region} specializing in {vibe}:"
    ),
    "illustrator": (
        "Here is the personal portfolio of an Indian visual artist or editorial illustrator "
        "based in {region} creating {vibe} artwork:"
    ),
    "ui": (
        "Here is the personal portfolio of an independent product designer or UI/UX craftsman "
        "based in {region} with high craft in {vibe}:"
    ),
    "brand": (
        "Here is the portfolio of an independent brand identity designer from {region} "
        "creating bespoke visual identities in {vibe}:"
    ),
    "all": (
        "Here is the personal portfolio of an independent creative artist or musician "
        "based in {region} known for {vibe}:"
    ),
}
