# -*- coding: utf-8 -*-


HOOK = {}

MONSTERS =  {
             'fly':  {
                        'hp':6,
                        'xp':5,
                        'hit':5,
                        'triangles':1,
                        'circles':1,
                        'squares':0,
                        'halfsquares':0.3,
                        },
             'ogre':  {
                        'hp':35,
                        'xp':17,
                        'hit':7,
                        'triangles':1.5,
                        'circles':1,
                        'squares':0.3,
                        'halfsquares':1,
                        },
             'kraken':  {
                        'hp':50,
                        'xp':37,
                        'hit':12,
                        'triangles':1,
                        'circles':0.3,
                        'squares':1,
                        'halfsquares':1.5,
                        },
             'dragon':  {
                        'hp':100,
                        'xp':50,
                        'hit':25,
                        'triangles':0.3,
                        'circles':1.5,
                        'squares':1,
                        'halfsquares':1,
                        },
             'boss':  {
                        'hp':400,
                        'xp':150,
                        'hit':30,
                        'triangles':1,
                        'circles':1,
                        'squares':1,
                        'halfsquares':1,
                        }
            }

LEVELS = {
    
            1: {
                  'nextlevel':10,
                  'hp':15,
                  'mp':15,
                  'hit':5,
                  'heal':0,
                  'triangles':0,
                  'circles':0,
                  'squares':0,
                  'halfsquares':0,
                  'life':0,
                  'color':1,
                  },
            2: {
                  'nextlevel':20,
                  'hp':17,
                  'mp':17,
                  'hit':6,
                  'heal':6,
                  'triangles':7,
                  'circles':0,
                  'squares':0,
                  'halfsquares':0,
                  'life':0,
                  'color':2,
                  },
            3: {
                  'nextlevel':25,
                  'hp':20,
                  'mp':20,
                  'hit':9,
                  'heal':7,
                  'triangles':10,
                  'circles':0,
                  'squares':0,
                  'halfsquares':0,
                  'life':0,
                  'color':2,
                  },
            4: {
                  'nextlevel':30,
                  'hp':25,
                  'mp':25,
                  'hit':12,
                  'heal':9,
                  'triangles':12,
                  'circles':15,
                  'squares':15,
                  'halfsquares':0,
                  'life':0,
                  'color':3,
                  },
            5: {
                  'nextlevel':35,
                  'hp':32,
                  'mp':32,
                  'hit':18,
                  'heal':13,
                  'triangles':20,
                  'circles':20,
                  'squares':20,
                  'halfsquares':0,
                  'life':0,
                  'color':3,
                  },
            6: {
                  'nextlevel':40,
                  'hp':41,
                  'mp':41,
                  'hit':20,
                  'heal':17,
                  'triangles':22,
                  'circles':25,
                  'squares':25,
                  'halfsquares':40,
                  'life':0,
                  'color':4,
                  },
            7: {
                  'nextlevel':45,
                  'hp':52,
                  'mp':52,
                  'hit':25,
                  'heal':20,
                  'triangles':25,
                  'circles':30,
                  'squares':30,
                  'halfsquares':35,
                  'life':0,
                  'color':4,
                  },
            8: {
                  'nextlevel':50,
                  'hp':66,
                  'mp':66,
                  'hit':30,
                  'heal':25,
                  'triangles':35,
                  'circles':40,
                  'squares':40,
                  'halfsquares':50,
                  'life':46,
                  'color':4,
                  },
            9: {
                  'nextlevel':55,
                  'hp':81,
                  'mp':81,
                  'hit':32,
                  'heal':28,
                  'triangles':40,
                  'circles':45,
                  'squares':45,
                  'halfsquares':55,
                  'life':56,
                  'color':5,
                  },
            10: {
                  'nextlevel':None,
                  'hp':99,
                  'mp':99,
                  'hit':35,
                  'heal':35,
                  'triangles':45,
                  'circles':50,
                  'squares':50,
                  'halfsquares':60,
                  'life':70,
                  'color':5,
                  }
  }

ITEMS = {
    'potion':10,
    'dragon blood': 15,
    'honey': 10,
    'stone': 5
  }

MAGIC = {
    'triangles':    5,
    'circles':      10,
    'squares':      10,
    'halfsquares':  15,
    'heal':         5,
    'life':         25
  }

DROPS = {
      'fly':      'honey',
      'ogre':     'stone',
      'kraken':   'potion',
      'dragon':   'dragon blood'
}