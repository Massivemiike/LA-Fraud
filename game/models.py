from django.db import models
from accounts.models import User, Profile


class Item(models.Model):
    """Base model for all items in the game."""
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    image = models.CharField(max_length=255, blank=True, null=True)  # Path to image
    is_available = models.BooleanField(default=True)
    
    # Item types
    ITEM_TYPES = [
        ('weapon', 'Weapon'),
        ('armor', 'Armor'),
        ('medical', 'Medical Supply'),
        ('booster', 'Booster'),
        ('training', 'Training Enhancer'),
        ('temporary', 'Temporary Item'),
    ]
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    
    def __str__(self):
        return self.name


class Weapon(models.Model):
    """Weapons that can be equipped by players."""
    
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='weapon')
    attack_power = models.IntegerField()
    durability = models.IntegerField()
    
    # Weapon types
    WEAPON_TYPES = [
        ('firearm', 'Firearm'),
        ('melee', 'Melee'),
    ]
    weapon_type = models.CharField(max_length=10, choices=WEAPON_TYPES)
    
    def __str__(self):
        return f"{self.item.name} - {self.get_weapon_type_display()}"


class Armor(models.Model):
    """Armor that can be equipped by players."""
    
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='armor')
    defense_power = models.IntegerField()
    durability = models.IntegerField()
    
    def __str__(self):
        return f"{self.item.name} - Armor"


class MedicalSupply(models.Model):
    """Medical supplies that can heal life points."""
    
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='medical_supply')
    healing_amount = models.IntegerField()
    
    def __str__(self):
        return f"{self.item.name} - Heals {self.healing_amount}"


class Booster(models.Model):
    """Items that boost player stats temporarily."""
    
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='booster')
    
    # Booster types
    BOOSTER_TYPES = [
        ('energy', 'Energy'),
        ('mood', 'Mood'),
        ('cooldown', 'Cooldown Reduction'),
    ]
    booster_type = models.CharField(max_length=10, choices=BOOSTER_TYPES)
    boost_amount = models.IntegerField()
    duration = models.IntegerField(help_text="Duration in minutes")
    
    def __str__(self):
        return f"{self.item.name} - {self.get_booster_type_display()} Booster"


class TrainingEnhancer(models.Model):
    """Items that improve gym gains."""
    
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='training_enhancer')
    enhancement_percentage = models.IntegerField(help_text="Percentage increase in gym gains")
    duration = models.IntegerField(help_text="Duration in minutes")
    
    def __str__(self):
        return f"{self.item.name} - Training Enhancer"


class TemporaryItem(models.Model):
    """Temporary items used in battles."""
    
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='temporary_item')
    
    # Effect types
    EFFECT_TYPES = [
        ('attack', 'Attack Boost'),
        ('defense', 'Defense Boost'),
        ('damage', 'Direct Damage'),
    ]
    effect_type = models.CharField(max_length=10, choices=EFFECT_TYPES)
    effect_amount = models.IntegerField()
    
    def __str__(self):
        return f"{self.item.name} - {self.get_effect_type_display()}"


class Inventory(models.Model):
    """Player's inventory of items."""
    
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='inventory')
    items = models.ManyToManyField(Item, through='InventoryItem')
    
    def __str__(self):
        return f"{self.profile.user.username_display}'s Inventory"


class InventoryItem(models.Model):
    """Relationship between Inventory and Item with quantity."""
    
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    equipped = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.inventory.profile.user.username_display} - {self.item.name} x{self.quantity}"


class Property(models.Model):
    """Real estate properties that players can own."""
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    image = models.CharField(max_length=255, blank=True, null=True)  # Path to image
    
    # Property benefits
    happiness_bonus = models.IntegerField(default=0)
    income_per_day = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Property types
    PROPERTY_TYPES = [
        ('home', 'Home'),
        ('business', 'Business'),
        ('vault', 'Vault'),
    ]
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES)
    
    # For vaults
    storage_capacity = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.name} - {self.get_property_type_display()}"


class OwnedProperty(models.Model):
    """Properties owned by players."""
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owned_properties')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    
    # For vaults
    stored_money = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.profile.user.username_display} - {self.property.name}"


class Location(models.Model):
    """Locations in the game world."""
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=255, blank=True, null=True)  # Path to image
    
    # Travel requirements
    travel_cost = models.DecimalField(max_digits=15, decimal_places=2)
    travel_time = models.IntegerField(help_text="Travel time in minutes")
    
    def __str__(self):
        return self.name


class Mission(models.Model):
    """Missions that players can complete."""
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='missions')
    
    # Mission requirements
    required_level = models.IntegerField(default=1)
    required_strength = models.IntegerField(default=0)
    required_speed = models.IntegerField(default=0)
    required_dexterity = models.IntegerField(default=0)
    required_defense = models.IntegerField(default=0)
    
    # Mission rewards
    experience_reward = models.IntegerField()
    money_reward = models.DecimalField(max_digits=15, decimal_places=2)
    item_rewards = models.ManyToManyField(Item, blank=True)
    
    # Mission types
    MISSION_TYPES = [
        ('combat', 'Combat'),
        ('delivery', 'Delivery'),
        ('crime', 'Crime'),
        ('police', 'Police'),
    ]
    mission_type = models.CharField(max_length=10, choices=MISSION_TYPES)
    
    # Mission difficulty
    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('extreme', 'Extreme'),
    ]
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    
    # Mission cooldown
    cooldown = models.IntegerField(help_text="Cooldown time in minutes")
    
    def __str__(self):
        return f"{self.name} - {self.get_difficulty_display()}"


class CompletedMission(models.Model):
    """Missions completed by players."""
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='completed_missions')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    completion_date = models.DateTimeField(auto_now_add=True)
    next_available_time = models.DateTimeField()
    
    def __str__(self):
        return f"{self.profile.user.username_display} - {self.mission.name}"


class Gang(models.Model):
    """Gangs that players can create and join."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.CharField(max_length=255, blank=True, null=True)  # Path to image
    
    # Gang type (criminal gang or police task force)
    GANG_TYPES = [
        ('criminal', 'Criminal Gang'),
        ('police', 'Police Task Force'),
    ]
    gang_type = models.CharField(max_length=10, choices=GANG_TYPES)
    
    # Gang stats
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    money = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Gang creation date
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_gang_type_display()}"


class GangMember(models.Model):
    """Members of gangs."""
    
    gang = models.ForeignKey(Gang, on_delete=models.CASCADE, related_name='members')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='gang_memberships')
    
    # Member roles
    ROLE_CHOICES = [
        ('leader', 'Leader'),
        ('officer', 'Officer'),
        ('member', 'Member'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    
    # Join date
    join_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.username_display} - {self.gang.name} - {self.get_role_display()}"


class Crime(models.Model):
    """Crimes that players can commit."""
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    # Crime requirements
    required_level = models.IntegerField(default=1)
    required_strength = models.IntegerField(default=0)
    required_speed = models.IntegerField(default=0)
    required_dexterity = models.IntegerField(default=0)
    required_defense = models.IntegerField(default=0)
    energy_cost = models.IntegerField()
    
    # Crime rewards
    experience_reward = models.IntegerField()
    money_reward_min = models.DecimalField(max_digits=15, decimal_places=2)
    money_reward_max = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Crime risks
    jail_risk = models.IntegerField(help_text="Percentage chance of going to jail")
    jail_time = models.IntegerField(help_text="Jail time in minutes if caught")
    
    # Crime cooldown
    cooldown = models.IntegerField(help_text="Cooldown time in minutes")
    
    def __str__(self):
        return self.name


class CommittedCrime(models.Model):
    """Crimes committed by players."""
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='committed_crimes')
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)
    
    # Crime result
    success = models.BooleanField()
    money_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    experience_earned = models.IntegerField(default=0)
    
    # Crime date
    date = models.DateTimeField(auto_now_add=True)
    next_available_time = models.DateTimeField()
    
    def __str__(self):
        result = "Success" if self.success else "Failure"
        return f"{self.profile.user.username_display} - {self.crime.name} - {result}"


class Gym(models.Model):
    """Gyms where players can train their stats."""
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=255, blank=True, null=True)  # Path to image
    
    # Gym requirements
    required_level = models.IntegerField(default=1)
    
    # Gym effectiveness
    effectiveness = models.FloatField(help_text="Multiplier for stat gains")
    
    # Gym cost
    cost_per_session = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return self.name


class GymSession(models.Model):
    """Gym sessions completed by players."""
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='gym_sessions')
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    
    # Stats trained
    STAT_CHOICES = [
        ('strength', 'Strength'),
        ('speed', 'Speed'),
        ('dexterity', 'Dexterity'),
        ('defense', 'Defense'),
    ]
    stat_trained = models.CharField(max_length=10, choices=STAT_CHOICES)
    
    # Session details
    energy_used = models.IntegerField()
    stat_gain = models.IntegerField()
    
    # Session date
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.username_display} - {self.gym.name} - {self.get_stat_trained_display()}"


class Battle(models.Model):
    """Battles between players."""
    
    attacker = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='battles_as_attacker')
    defender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='battles_as_defender')
    
    # Battle result
    attacker_won = models.BooleanField()
    
    # Battle rewards
    money_stolen = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    experience_gained = models.IntegerField()
    
    # Battle details
    attacker_damage_dealt = models.IntegerField()
    defender_damage_dealt = models.IntegerField()
    
    # Battle date
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        winner = self.attacker.user.username_display if self.attacker_won else self.defender.user.username_display
        return f"{self.attacker.user.username_display} vs {self.defender.user.username_display} - Winner: {winner}"


class Bounty(models.Model):
    """Bounties placed on players."""
    
    target = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='bounties_on_me')
    placer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='bounties_placed')
    
    # Bounty details
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    
    # Bounty status
    is_active = models.BooleanField(default=True)
    
    # Bounty dates
    placed_date = models.DateTimeField(auto_now_add=True)
    claimed_date = models.DateTimeField(null=True, blank=True)
    claimed_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='bounties_claimed')
    
    def __str__(self):
        return f"Bounty on {self.target.user.username_display} - ${self.amount}"


class StockMarket(models.Model):
    """Stock market where players can buy and sell stocks."""
    
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    
    # Stock price
    current_price = models.DecimalField(max_digits=15, decimal_places=2)
    previous_price = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Stock details
    total_shares = models.IntegerField()
    available_shares = models.IntegerField()
    
    # Stock dividend
    dividend_percentage = models.FloatField(default=0)
    next_dividend_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.name} ({self.symbol})"


class StockOwnership(models.Model):
    """Stocks owned by players."""
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owned_stocks')
    stock = models.ForeignKey(StockMarket, on_delete=models.CASCADE)
    
    # Ownership details
    shares = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Purchase date
    purchase_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.username_display} - {self.stock.symbol} - {self.shares} shares"


class Achievement(models.Model):
    """Achievements that players can earn."""
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    # Achievement requirements
    REQUIREMENT_TYPES = [
        ('crimes', 'Crimes Committed'),
        ('battles', 'Battles Won'),
        ('missions', 'Missions Completed'),
        ('level', 'Level Reached'),
        ('money', 'Money Earned'),
        ('properties', 'Properties Owned'),
    ]
    requirement_type = models.CharField(max_length=20, choices=REQUIREMENT_TYPES)
    requirement_value = models.IntegerField()
    
    # Achievement rewards
    knowledge_points_reward = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name


class EarnedAchievement(models.Model):
    """Achievements earned by players."""
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='earned_achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    
    # Earned date
    earned_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.username_display} - {self.achievement.name}"