"""
Service d'Analytics pour L'Univers est au Carré.

Collecte et analyse les statistiques de visiteurs:
- Géolocalisation (pays, ville) via IP
- Nombre de visites par période
- Type d'appareil
- Pages visitées
"""
import os
import httpx
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorClient
from user_agents import parse as parse_user_agent

logger = logging.getLogger(__name__)

# Configuration MongoDB
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "univers_carre")

# Client MongoDB async
_client: Optional[AsyncIOMotorClient] = None
_db = None

def get_analytics_db():
    """Récupère la connexion à la base de données."""
    global _client, _db
    if _client is None:
        _client = AsyncIOMotorClient(MONGO_URL)
        _db = _client[DB_NAME]
    return _db

# Cache pour la géolocalisation (éviter trop de requêtes API)
_geo_cache: Dict[str, Dict] = {}


async def get_geolocation(ip: str) -> Dict[str, Any]:
    """
    Récupère la géolocalisation d'une IP via ip-api.com (gratuit).
    Utilise un cache pour éviter les requêtes répétées.
    """
    # Ignorer les IPs locales
    if ip in ["127.0.0.1", "localhost", "::1"] or ip.startswith("10.") or ip.startswith("192.168."):
        return {
            "country": "Local",
            "countryCode": "LO",
            "city": "Localhost",
            "region": "Local",
            "lat": 0,
            "lon": 0,
            "isp": "Local Network"
        }
    
    # Vérifier le cache
    if ip in _geo_cache:
        return _geo_cache[ip]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,region,city,lat,lon,isp",
                timeout=5.0
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    geo_data = {
                        "country": data.get("country", "Inconnu"),
                        "countryCode": data.get("countryCode", "XX"),
                        "city": data.get("city", "Inconnu"),
                        "region": data.get("region", ""),
                        "lat": data.get("lat", 0),
                        "lon": data.get("lon", 0),
                        "isp": data.get("isp", "")
                    }
                    # Mettre en cache (limiter la taille du cache)
                    if len(_geo_cache) < 10000:
                        _geo_cache[ip] = geo_data
                    return geo_data
    except Exception as e:
        logger.warning(f"Erreur géolocalisation pour {ip}: {e}")
    
    return {
        "country": "Inconnu",
        "countryCode": "XX",
        "city": "Inconnu",
        "region": "",
        "lat": 0,
        "lon": 0,
        "isp": ""
    }


def parse_device_info(user_agent_string: str) -> Dict[str, str]:
    """Parse le User-Agent pour extraire les informations d'appareil."""
    try:
        ua = parse_user_agent(user_agent_string)
        return {
            "device_type": "mobile" if ua.is_mobile else ("tablet" if ua.is_tablet else "desktop"),
            "browser": f"{ua.browser.family} {ua.browser.version_string}",
            "os": f"{ua.os.family} {ua.os.version_string}",
            "is_bot": ua.is_bot
        }
    except:
        return {
            "device_type": "unknown",
            "browser": "unknown",
            "os": "unknown",
            "is_bot": False
        }


async def record_visit(
    ip: str,
    path: str,
    method: str,
    user_agent: str,
    referer: Optional[str] = None,
    user_email: Optional[str] = None
) -> None:
    """
    Enregistre une visite dans la base de données.
    """
    db = get_analytics_db()
    
    # Obtenir la géolocalisation
    geo = await get_geolocation(ip)
    
    # Parser le User-Agent
    device = parse_device_info(user_agent)
    
    # Ne pas enregistrer les bots
    if device["is_bot"]:
        return
    
    # Créer l'enregistrement
    visit = {
        "timestamp": datetime.now(timezone.utc),
        "ip": ip,
        "path": path,
        "method": method,
        "country": geo["country"],
        "country_code": geo["countryCode"],
        "city": geo["city"],
        "region": geo["region"],
        "lat": geo["lat"],
        "lon": geo["lon"],
        "isp": geo["isp"],
        "device_type": device["device_type"],
        "browser": device["browser"],
        "os": device["os"],
        "referer": referer,
        "user_email": user_email
    }
    
    try:
        await db.analytics.insert_one(visit)
    except Exception as e:
        logger.error(f"Erreur enregistrement visite: {e}")


async def get_analytics_summary() -> Dict[str, Any]:
    """
    Récupère un résumé des statistiques.
    """
    db = get_analytics_db()
    now = datetime.now(timezone.utc)
    
    # Périodes
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    # Compter les visites
    total = await db.analytics.count_documents({})
    today = await db.analytics.count_documents({"timestamp": {"$gte": today_start}})
    last_7_days = await db.analytics.count_documents({"timestamp": {"$gte": week_ago}})
    last_30_days = await db.analytics.count_documents({"timestamp": {"$gte": month_ago}})
    
    # Visiteurs uniques (par IP)
    unique_total = len(await db.analytics.distinct("ip"))
    unique_today = len(await db.analytics.distinct("ip", {"timestamp": {"$gte": today_start}}))
    unique_7_days = len(await db.analytics.distinct("ip", {"timestamp": {"$gte": week_ago}}))
    unique_30_days = len(await db.analytics.distinct("ip", {"timestamp": {"$gte": month_ago}}))
    
    return {
        "total_visits": total,
        "visits_today": today,
        "visits_7_days": last_7_days,
        "visits_30_days": last_30_days,
        "unique_visitors_total": unique_total,
        "unique_visitors_today": unique_today,
        "unique_visitors_7_days": unique_7_days,
        "unique_visitors_30_days": unique_30_days,
        "generated_at": now.isoformat()
    }


async def get_visitors_by_country(days: int = 30, limit: int = 20) -> List[Dict]:
    """
    Récupère les statistiques par pays.
    """
    db = get_analytics_db()
    since = datetime.now(timezone.utc) - timedelta(days=days)
    
    pipeline = [
        {"$match": {"timestamp": {"$gte": since}}},
        {"$group": {
            "_id": {"country": "$country", "country_code": "$country_code"},
            "visits": {"$sum": 1},
            "unique_ips": {"$addToSet": "$ip"}
        }},
        {"$project": {
            "country": "$_id.country",
            "country_code": "$_id.country_code",
            "visits": 1,
            "unique_visitors": {"$size": "$unique_ips"}
        }},
        {"$sort": {"visits": -1}},
        {"$limit": limit}
    ]
    
    results = await db.analytics.aggregate(pipeline).to_list(length=limit)
    return [{"country": r["country"], "country_code": r["country_code"], 
             "visits": r["visits"], "unique_visitors": r["unique_visitors"]} for r in results]


async def get_visitors_by_city(days: int = 30, limit: int = 20) -> List[Dict]:
    """
    Récupère les statistiques par ville.
    """
    db = get_analytics_db()
    since = datetime.now(timezone.utc) - timedelta(days=days)
    
    pipeline = [
        {"$match": {"timestamp": {"$gte": since}}},
        {"$group": {
            "_id": {"city": "$city", "country": "$country"},
            "visits": {"$sum": 1},
            "unique_ips": {"$addToSet": "$ip"}
        }},
        {"$project": {
            "city": "$_id.city",
            "country": "$_id.country",
            "visits": 1,
            "unique_visitors": {"$size": "$unique_ips"}
        }},
        {"$sort": {"visits": -1}},
        {"$limit": limit}
    ]
    
    results = await db.analytics.aggregate(pipeline).to_list(length=limit)
    return [{"city": r["city"], "country": r["country"], 
             "visits": r["visits"], "unique_visitors": r["unique_visitors"]} for r in results]


async def get_visits_timeline(days: int = 30) -> List[Dict]:
    """
    Récupère la timeline des visites par jour.
    """
    db = get_analytics_db()
    since = datetime.now(timezone.utc) - timedelta(days=days)
    
    pipeline = [
        {"$match": {"timestamp": {"$gte": since}}},
        {"$group": {
            "_id": {
                "year": {"$year": "$timestamp"},
                "month": {"$month": "$timestamp"},
                "day": {"$dayOfMonth": "$timestamp"}
            },
            "visits": {"$sum": 1},
            "unique_ips": {"$addToSet": "$ip"}
        }},
        {"$project": {
            "date": {
                "$dateFromParts": {
                    "year": "$_id.year",
                    "month": "$_id.month",
                    "day": "$_id.day"
                }
            },
            "visits": 1,
            "unique_visitors": {"$size": "$unique_ips"}
        }},
        {"$sort": {"date": 1}}
    ]
    
    results = await db.analytics.aggregate(pipeline).to_list(length=days + 1)
    return [{"date": r["date"].strftime("%Y-%m-%d"), 
             "visits": r["visits"], 
             "unique_visitors": r["unique_visitors"]} for r in results]


async def get_top_pages(days: int = 30, limit: int = 20) -> List[Dict]:
    """
    Récupère les pages les plus visitées.
    """
    db = get_analytics_db()
    since = datetime.now(timezone.utc) - timedelta(days=days)
    
    pipeline = [
        {"$match": {"timestamp": {"$gte": since}}},
        {"$group": {
            "_id": "$path",
            "visits": {"$sum": 1}
        }},
        {"$sort": {"visits": -1}},
        {"$limit": limit}
    ]
    
    results = await db.analytics.aggregate(pipeline).to_list(length=limit)
    return [{"path": r["_id"], "visits": r["visits"]} for r in results]


async def get_device_stats(days: int = 30) -> Dict[str, int]:
    """
    Récupère les statistiques par type d'appareil.
    """
    db = get_analytics_db()
    since = datetime.now(timezone.utc) - timedelta(days=days)
    
    pipeline = [
        {"$match": {"timestamp": {"$gte": since}}},
        {"$group": {
            "_id": "$device_type",
            "count": {"$sum": 1}
        }}
    ]
    
    results = await db.analytics.aggregate(pipeline).to_list(length=10)
    return {r["_id"]: r["count"] for r in results if r["_id"]}


async def get_monthly_stats(months: int = 12) -> List[Dict]:
    """
    Récupère les statistiques mensuelles.
    """
    db = get_analytics_db()
    since = datetime.now(timezone.utc) - timedelta(days=months * 30)
    
    pipeline = [
        {"$match": {"timestamp": {"$gte": since}}},
        {"$group": {
            "_id": {
                "year": {"$year": "$timestamp"},
                "month": {"$month": "$timestamp"}
            },
            "visits": {"$sum": 1},
            "unique_ips": {"$addToSet": "$ip"}
        }},
        {"$project": {
            "year": "$_id.year",
            "month": "$_id.month",
            "visits": 1,
            "unique_visitors": {"$size": "$unique_ips"}
        }},
        {"$sort": {"year": 1, "month": 1}}
    ]
    
    results = await db.analytics.aggregate(pipeline).to_list(length=months + 1)
    
    month_names = ["", "Jan", "Fév", "Mar", "Avr", "Mai", "Juin", 
                   "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]
    
    return [{
        "period": f"{month_names[r['month']]} {r['year']}",
        "visits": r["visits"],
        "unique_visitors": r["unique_visitors"]
    } for r in results]
