import logging
logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)

import json
import os
import time

from diskcache import Cache 

# Import app to get api_config
def get_beh_config(behaviour_type, behaviour_id):
    import requests
    from requests.auth import HTTPBasicAuth
    from flask import current_app as app

    #TODO: Generalise AUTH config: change VEDA_USER to User and so on.
    api_config = app.config
    Veda_auth = HTTPBasicAuth(api_config['VEDA_USER'], api_config['VEDA_PASSWORD'])

    final_url = "{}/{}/{}/{}".format(api_config['VEDA_SERVER_URL'], api_config['VEDA_API_VERSION'], behaviour_type, behaviour_id)     
    logging.info("Fetching Behaviour config: {}".format(final_url))

    resp = {}
    try:
        resp = requests.get(final_url, auth=Veda_auth, timeout=10)
        resp.raise_for_status()
        resp = resp.json()
        cache_config(behaviour_id,resp)
    except Exception as e:
        logging.error("getConfig Failed:{}. Using cached config.".format(e))
        resp = get_cached_config(behaviour_id)
    if resp is None:
        raise RuntimeError("Failed to fetch cloud config for behaviour {}".format(behaviour_id))

    if(behaviour_type is "cameras"):
        resp['enabled'] = resp.get("isEnabled",True)
    else:
        resp['enabled'] = resp.get("params",{}).get("enable",True)
        
    return resp

# Cached config file name 
def _get_cached_config_key(behaviour_id):
    key = "config_{}".format(behaviour_id)
    return key

# Cache config to file
def cache_config(behaviour_id,config):
    key = _get_cached_config_key(behaviour_id)
    # config_cache_validity in days with float value data type, default 7 days.
    expire_time = config.get("params",{}).get("config_cache_validity",7) 
    cache = Cache(directory="/persistant_cache")
    cache.set(key, value=config,expire=int(expire_time*24*60*60))
    return config

# Retrieve cached config from file
def get_cached_config(behaviour_id):
    key = _get_cached_config_key(behaviour_id)
    cache = Cache(directory="/persistant_cache")
    config = cache.get(key,None)
    if config is not None:
        # config_cache_disable boolen param for disabling cache.By default caching is enabled
        if config.get("params",{}).get("config_cache_disable",False):   
            config=None
            logger.info("cached config disabled for id: {}".format(behaviour_id))
    else:
        logger.info("valid cached config not found for id: {}".format(behaviour_id))
    return config

class Behaviour(object):
    def __init__(self, config, behaviour_id=None, behaviour_type="behaviours"):
        
        if behaviour_id:
            config = get_beh_config(behaviour_type=behaviour_type, behaviour_id=behaviour_id)
        
        self.id = config["_id"]
        self.offlineMode = not bool(behaviour_id)
        self.config  = config
        self.enabled = config.get("enabled",True)

    ###### Update Related Functions
    # Topics to be subscribed
    def subscriptionTopics(self,subscriptions=[]):
        if not self.offlineMode: # If config is online based
            if "camera" in self.config:
                # Behaviour update subscription
                subscriptions.append(
                    {
                        "_id": self.id,
                        'topic':'behaviours',
                        'eventType': 'Updated'
                    }
                )        
                subscriptions.append(
                    {
                        "_id": self.id,
                        'topic':'behaviours',
                        'eventType': 'Replaced'
                    }
                )
            # Camera update subscription
            # if type is behaviour
            if "camera" in self.config:
                camera_id = self.config["camera"]
                # Handle embedded=True case
                if type(camera_id) == dict:    
                    camera_id = camera_id["_id"]
            else:
                camera_id = self.id
            
            subscriptions.append(
                {
                    "_id": camera_id,
                    'topic':'cameras',
                    'eventType': 'Updated'
                }
            ) 
            subscriptions.append(
                {
                    "_id": camera_id,
                    'topic':'cameras',
                    'eventType': 'Replaced'
                }
            ) 

        return subscriptions

    # update event callback
    def update(self, data):
        logger.info("Behaviour: hot updates not handled by behaviour: {}. It will be handled via restart policy".format(self))
        UpdateSuccess = False
        return UpdateSuccess

    def run(self, data):
        return(data)
