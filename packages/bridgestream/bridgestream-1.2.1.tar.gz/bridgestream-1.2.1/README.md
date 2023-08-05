# BridgeStream 


BridgeStream is a order oriented binary serialization library developed for performance and efficiency.

BridgeStream is used as a part of an real-time online game to
transmit data between the client and servers.

You can encode/decode primitive types, collection on primitives, custom serializers and other BridgeStream's easily
and efficiently.


## Install

```bash
pip install bridgestream
```

## Basic Usage

Create a stream

```python
from bridgestream import BridgeStream

stream = BridgeStream()
```

Write some data

```python
stream.write_int(1)
stream.write_string("test")
stream.write_float(0.1)
stream.write_bool(True)
```

Encode

```python
data = stream.encode()
```

Decode

```python
stream = BridgeStream(data)
```

Read in order

```python
stream.read_int()  # 1
stream.read_string()  # test
stream.read_float()  # 0.1
stream.read_bool()  # True
```

## Custom Types

You can define your own serializers to abstract your common data types using `BridgeSerializer`.

You must implement the `write` method of `BridgeSerializer` 
to be able to encode it as a **stream** and you must implement the `read` method to be able to decode it as a **stream**.

```python
from bridgestream import BridgeSerializer

@dataclass  # dataclass is not required but recommended
class Vector3(BridgeSerializer):
    x: int
    y: int
    z: int

    def write(self, stream: BridgeStream):
        stream.write_int(self.x)
        stream.write_int(self.y)
        stream.write_int(self.z)

    def read(self, stream: BridgeStream):
        self.x = stream.write_int(x)
        self.y = stream.write_int(y)
        self.z = stream.write_int(z)


```

You can encode custom serializers using the `write` method of 
`BridgeStream`.

```python

vector = Vector3(1, 0, 2)

stream = BridgeStream()
stream.write(vector)

data = stream.encode()
```

You can decode a custom serializer using the `read(BirdgeSerializer)` method of 
`BridgeStream`.

```python
stream = BridgeStream(data)

vector = stream.read(Vector3)  # Vector3(x=1, y=0, z=2)
```

You can also read/write list of custom serializers.
```python
vectors = [Vector3(1, 0, 2), Vector3(3, -1, 4)]

stream = BridgeStream()
stream.write_list(vector)

data = stream.encode()


stream = BridgeStream(data)

vector = stream.read_list(Vector3)  # [Vector3(x=1, y=0, z=2), ector3(x=3, y=-1, z=4)]
```


## Nested BridgeStream

Some times it is necessary to write a bridgestream within another bridgestream. In this example; we have 2 different serializers that have the same purposes. Each Serializer can do its business logic within its own read/write methods and still can be serialized as a whole.


Class definitions
```python

@dataclass
class WarriorLevel(BridgeSerializer):
    health: int
    attack_radious: int
    shield: int

    def write(self, stream: BridgeStream):
        stream.write_int(self.health)
        stream.write_int(self.attack_radious)
        stream.write_int(self.shield)

    def read(self, stream: BridgeStream):
        self.health = stream.read_int()
        self.attack_radious = stream.read_int()
        self.shield = stream.read_int()

@dataclass
class MageLevel(BridgeSerializer):
    health: int
    projectile_damage: int
    regeneration: int

    def write(self, stream: BridgeStream):
        stream.write_int(self.health)
        stream.write_int(self.projectile_damage)
        stream.write_int(self.regeneration)

    def read(self, stream: BridgeStream):
        self.health = stream.read_int()
        self.projectile_damage = stream.read_int()
        self.regeneration = stream.read_int()


@dataclass
class Warrior(BridgeSerializer):
    id: str
    attack_speed: float
    atack_cooldown: float
    levels: List[WarriorLevel]

    def write(self, stream):
        stream.write_string(self.id)
        stream.write_float(self.attack_speed)
        stream.write_float(self.atack_cooldown)
        stream.write_list(self.levels)


    def read(self, stream):
        self.id = stream.read_string()
        self.attack_speed = stream.read_float()
        self.atack_cooldown = stream.read_float()
        self.levels = stream.read_list(WarriorLevel)


@dataclass
class Mage(BridgeSerializer):
    id: str
    projectile_range: float
    projectile_speed: float
    levels: List[MageLevel]

    def write(self, stream: BridgeStream):
        stream.write_string(self.id)
        stream.write_float(self.projectile_range)
        stream.write_float(self.projectile_speed)
        stream.write_list(self.levels)


    def read(self, stream: BridgeStream):
        self.id = stream.read_string()
        self.attack_speed = stream.read_float()
        self.atack_cooldown = stream.read_float()
        self.levels = stream.read_list(MageLevel)


@dataclass
class Player(BridgeSerializer):
    name: str
    level: int
    heroes: List[str]

    def write(self, stream: BridgeStream):
        stream.write_string(self.name)
        stream.write_int(self.level)
        stream.write_string_list(self.heroes)


    def read(self, stream: BridgeStream):
        self.name = stream.read_string()
        self.level = stream.read_int()
        self.heroes = stream.read_string_list()
```

Initialization

```python

player = Player(name="player-1", level=5, heroes=["w-1", "m-1"])

hero_cofigurations = {
    "warrior": Warrior(
        id="w-1",
        attack_speed=0.4,
        atack_cooldown=0.2,
        levels=[WarriorLevel(300, 50, 1), WarriorLevel(340, 55, 1.2)]
    ),
    "mage": Mage(
        id="m-1",
        projectile_range=400,
        projectile_speed=1.4,
        levels=[MageLevel(1.5, 30, 5), MageLevel(340, 35, 10)]
    ),
}

```

Nested encoding & decoding

```python
stream = BridgeStream()
stream.write(player)

hero_config_stream = BridgeStream()
for class_name, config in hero_cofigurations.items():
    hero_config_stream.write_string(class_name)
    hero_config_stream.write(config)

stream.write_stream(hero_config_stream)

data = stream.encode()


stream = BridgeStream(data)

player = stream.read(Player)  # Player(name="player-1", level=5, heroes=["w-1", "m-1"])

# Read the stream to the end and create config by types

hero_classes = {"warrior": Warrior, "mage": Mage}
hero_cofigurations = {}
while stream.has_more():
    class_name = stream.read_string()
    config = stream.read(hero_classes[class_name])
    hero_cofigurations[class_name] = config


hero_cofigurations
"""
{
    "warrior": Warrior(
        id="w-1",
        attack_speed=0.4,
        atack_cooldown=0.2,
        levels=[WarriorLevel(300, 50, 1), WarriorLevel(340, 55, 1.2)]
    ),
    "mage": Mage(
        id="m-1",
        projectile_range=400,
        projectile_speed=1.4,
        levels=[MageLevel(1.5, 30, 5), MageLevel(340, 35, 10)]
    ),
}
"""
```
