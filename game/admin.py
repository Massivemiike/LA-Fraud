from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Item, Weapon, Armor, MedicalSupply, Booster, TrainingEnhancer, TemporaryItem,
    Inventory, InventoryItem, Property, OwnedProperty, Location, Mission, CompletedMission,
    Gang, GangMember, Crime, CommittedCrime, Gym, GymSession, Battle, Bounty,
    StockMarket, StockOwnership, Achievement, EarnedAchievement
)


class WeaponInline(admin.StackedInline):
    model = Weapon
    can_delete = False
    verbose_name_plural = 'Weapon Details'


class ArmorInline(admin.StackedInline):
    model = Armor
    can_delete = False
    verbose_name_plural = 'Armor Details'


class MedicalSupplyInline(admin.StackedInline):
    model = MedicalSupply
    can_delete = False
    verbose_name_plural = 'Medical Supply Details'


class BoosterInline(admin.StackedInline):
    model = Booster
    can_delete = False
    verbose_name_plural = 'Booster Details'


class TrainingEnhancerInline(admin.StackedInline):
    model = TrainingEnhancer
    can_delete = False
    verbose_name_plural = 'Training Enhancer Details'


class TemporaryItemInline(admin.StackedInline):
    model = TemporaryItem
    can_delete = False
    verbose_name_plural = 'Temporary Item Details'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'price', 'is_available')
    list_filter = ('item_type', 'is_available')
    search_fields = ('name', 'description')
    
    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        
        if obj.item_type == 'weapon':
            return [WeaponInline]
        elif obj.item_type == 'armor':
            return [ArmorInline]
        elif obj.item_type == 'medical':
            return [MedicalSupplyInline]
        elif obj.item_type == 'booster':
            return [BoosterInline]
        elif obj.item_type == 'training':
            return [TrainingEnhancerInline]
        elif obj.item_type == 'temporary':
            return [TemporaryItemInline]
        
        return []


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('profile',)
    search_fields = ('profile__user__email', 'profile__user__username_display')


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('inventory', 'item', 'quantity', 'equipped')
    list_filter = ('equipped',)
    search_fields = ('inventory__profile__user__username_display', 'item__name')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_type', 'price', 'income_per_day')
    list_filter = ('property_type',)
    search_fields = ('name', 'description')


@admin.register(OwnedProperty)
class OwnedPropertyAdmin(admin.ModelAdmin):
    list_display = ('profile', 'property', 'purchase_date')
    search_fields = ('profile__user__username_display', 'property__name')
    date_hierarchy = 'purchase_date'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'travel_cost', 'travel_time')
    search_fields = ('name', 'description')


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'mission_type', 'difficulty', 'required_level')
    list_filter = ('mission_type', 'difficulty', 'location')
    search_fields = ('name', 'description')
    filter_horizontal = ('item_rewards',)


@admin.register(CompletedMission)
class CompletedMissionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'mission', 'completion_date', 'next_available_time')
    search_fields = ('profile__user__username_display', 'mission__name')
    date_hierarchy = 'completion_date'


@admin.register(Gang)
class GangAdmin(admin.ModelAdmin):
    list_display = ('name', 'gang_type', 'level', 'money')
    list_filter = ('gang_type',)
    search_fields = ('name', 'description')


@admin.register(GangMember)
class GangMemberAdmin(admin.ModelAdmin):
    list_display = ('profile', 'gang', 'role', 'join_date')
    list_filter = ('role', 'gang')
    search_fields = ('profile__user__username_display', 'gang__name')
    date_hierarchy = 'join_date'


@admin.register(Crime)
class CrimeAdmin(admin.ModelAdmin):
    list_display = ('name', 'required_level', 'energy_cost', 'jail_risk', 'jail_time')
    search_fields = ('name', 'description')


@admin.register(CommittedCrime)
class CommittedCrimeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'crime', 'success', 'money_earned', 'date')
    list_filter = ('success',)
    search_fields = ('profile__user__username_display', 'crime__name')
    date_hierarchy = 'date'


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'required_level', 'effectiveness', 'cost_per_session')
    search_fields = ('name', 'description')


@admin.register(GymSession)
class GymSessionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'gym', 'stat_trained', 'energy_used', 'stat_gain', 'date')
    list_filter = ('stat_trained', 'gym')
    search_fields = ('profile__user__username_display', 'gym__name')
    date_hierarchy = 'date'


@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = ('attacker', 'defender', 'attacker_won', 'money_stolen', 'experience_gained', 'date')
    list_filter = ('attacker_won',)
    search_fields = ('attacker__user__username_display', 'defender__user__username_display')
    date_hierarchy = 'date'


@admin.register(Bounty)
class BountyAdmin(admin.ModelAdmin):
    list_display = ('target', 'placer', 'amount', 'is_active', 'placed_date')
    list_filter = ('is_active',)
    search_fields = ('target__user__username_display', 'placer__user__username_display')
    date_hierarchy = 'placed_date'


@admin.register(StockMarket)
class StockMarketAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'current_price', 'previous_price', 'dividend_percentage')
    search_fields = ('name', 'symbol', 'description')


@admin.register(StockOwnership)
class StockOwnershipAdmin(admin.ModelAdmin):
    list_display = ('profile', 'stock', 'shares', 'purchase_price', 'purchase_date')
    search_fields = ('profile__user__username_display', 'stock__name', 'stock__symbol')
    date_hierarchy = 'purchase_date'


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'requirement_type', 'requirement_value', 'knowledge_points_reward')
    list_filter = ('requirement_type',)
    search_fields = ('name', 'description')


@admin.register(EarnedAchievement)
class EarnedAchievementAdmin(admin.ModelAdmin):
    list_display = ('profile', 'achievement', 'earned_date')
    search_fields = ('profile__user__username_display', 'achievement__name')
    date_hierarchy = 'earned_date'