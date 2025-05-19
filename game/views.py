from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from accounts.models import Profile
from .models import (
    Item, Inventory, InventoryItem, Property, OwnedProperty, Location, Mission, CompletedMission,
    Gang, GangMember, Crime, CommittedCrime, Gym, GymSession, Battle, Bounty,
    StockMarket, StockOwnership, Achievement, EarnedAchievement
)


@login_required
def game_home(request):
    """Home page for the game."""
    profile = request.user.profile
    
    # Get player stats
    stats = {
        'level': profile.level,
        'experience': profile.experience,
        'life': profile.life,
        'max_life': profile.max_life,
        'energy': profile.energy,
        'max_energy': profile.max_energy,
        'endurance': profile.endurance,
        'max_endurance': profile.max_endurance,
        'mood': profile.mood,
        'max_mood': profile.max_mood,
        'knowledge_points': profile.knowledge_points,
        'money': profile.money,
        'bank_money': profile.bank_money,
        'current_location': profile.current_location,
    }
    
    # Check if player is in jail or hospital
    status = {
        'is_in_jail': profile.is_in_jail,
        'jail_release_time': profile.jail_release_time,
        'is_in_hospital': profile.is_in_hospital,
        'hospital_release_time': profile.hospital_release_time,
    }
    
    # Check if player can be released from jail or hospital
    now = timezone.now()
    if profile.is_in_jail and profile.jail_release_time and profile.jail_release_time <= now:
        profile.is_in_jail = False
        profile.jail_release_time = None
        profile.save()
        messages.success(request, 'You have been released from jail!')
        status['is_in_jail'] = False
    
    if profile.is_in_hospital and profile.hospital_release_time and profile.hospital_release_time <= now:
        profile.is_in_hospital = False
        profile.hospital_release_time = None
        profile.save()
        messages.success(request, 'You have been released from the hospital!')
        status['is_in_hospital'] = False
    
    # Get recent activities
    recent_crimes = CommittedCrime.objects.filter(profile=profile).order_by('-date')[:5]
    recent_missions = CompletedMission.objects.filter(profile=profile).order_by('-completion_date')[:5]
    recent_battles = Battle.objects.filter(attacker=profile).order_by('-date')[:5]
    
    context = {
        'profile': profile,
        'stats': stats,
        'status': status,
        'recent_crimes': recent_crimes,
        'recent_missions': recent_missions,
        'recent_battles': recent_battles,
    }
    
    return render(request, 'game/home.html', context)


@login_required
def inventory(request):
    """View for player's inventory."""
    profile = request.user.profile
    
    # Get or create inventory
    inventory, created = Inventory.objects.get_or_create(profile=profile)
    
    # Get inventory items
    inventory_items = InventoryItem.objects.filter(inventory=inventory)
    
    context = {
        'profile': profile,
        'inventory': inventory,
        'inventory_items': inventory_items,
    }
    
    return render(request, 'game/inventory.html', context)


@login_required
def shop(request):
    """View for the shop."""
    profile = request.user.profile
    
    # Get available items
    items = Item.objects.filter(is_available=True)
    
    context = {
        'profile': profile,
        'items': items,
    }
    
    return render(request, 'game/shop.html', context)


@login_required
def buy_item(request, item_id):
    """View for buying an item."""
    profile = request.user.profile
    item = get_object_or_404(Item, id=item_id, is_available=True)
    
    # Check if player has enough money
    if profile.money < item.price:
        messages.error(request, f"You don't have enough money to buy {item.name}.")
        return redirect('shop')
    
    # Get or create inventory
    inventory, created = Inventory.objects.get_or_create(profile=profile)
    
    # Check if player already has this item
    inventory_item, created = InventoryItem.objects.get_or_create(
        inventory=inventory,
        item=item,
        defaults={'quantity': 0}
    )
    
    # Update inventory item quantity
    inventory_item.quantity += 1
    inventory_item.save()
    
    # Update player's money
    profile.money -= item.price
    profile.save()
    
    messages.success(request, f"You have bought {item.name} for ${item.price}.")
    return redirect('inventory')


@login_required
def crimes(request):
    """View for crimes."""
    profile = request.user.profile
    
    # Check if player is in jail or hospital
    if profile.is_in_jail:
        messages.error(request, "You are in jail and cannot commit crimes.")
        return redirect('game_home')
    
    if profile.is_in_hospital:
        messages.error(request, "You are in the hospital and cannot commit crimes.")
        return redirect('game_home')
    
    # Get available crimes
    crimes = Crime.objects.filter(required_level__lte=profile.level)
    
    # Get committed crimes with cooldown
    committed_crimes = CommittedCrime.objects.filter(profile=profile)
    crime_cooldowns = {}
    
    for committed_crime in committed_crimes:
        if committed_crime.next_available_time > timezone.now():
            crime_cooldowns[committed_crime.crime.id] = committed_crime.next_available_time
    
    context = {
        'profile': profile,
        'crimes': crimes,
        'crime_cooldowns': crime_cooldowns,
    }
    
    return render(request, 'game/crimes.html', context)


@login_required
def missions(request):
    """View for missions."""
    profile = request.user.profile
    
    # Check if player is in jail or hospital
    if profile.is_in_jail:
        messages.error(request, "You are in jail and cannot do missions.")
        return redirect('game_home')
    
    if profile.is_in_hospital:
        messages.error(request, "You are in the hospital and cannot do missions.")
        return redirect('game_home')
    
    # Get available missions
    missions = Mission.objects.filter(required_level__lte=profile.level)
    
    # Get completed missions with cooldown
    completed_missions = CompletedMission.objects.filter(profile=profile)
    mission_cooldowns = {}
    
    for completed_mission in completed_missions:
        if completed_mission.next_available_time > timezone.now():
            mission_cooldowns[completed_mission.mission.id] = completed_mission.next_available_time
    
    context = {
        'profile': profile,
        'missions': missions,
        'mission_cooldowns': mission_cooldowns,
    }
    
    return render(request, 'game/missions.html', context)


@login_required
def gym(request):
    """View for the gym."""
    profile = request.user.profile
    
    # Check if player is in jail or hospital
    if profile.is_in_jail:
        messages.error(request, "You are in jail and cannot go to the gym.")
        return redirect('game_home')
    
    if profile.is_in_hospital:
        messages.error(request, "You are in the hospital and cannot go to the gym.")
        return redirect('game_home')
    
    # Get available gyms
    gyms = Gym.objects.filter(required_level__lte=profile.level)
    
    context = {
        'profile': profile,
        'gyms': gyms,
    }
    
    return render(request, 'game/gym.html', context)


@login_required
def properties(request):
    """View for properties."""
    profile = request.user.profile
    
    # Get available properties
    properties = Property.objects.all()
    
    # Get owned properties
    owned_properties = OwnedProperty.objects.filter(profile=profile)
    
    context = {
        'profile': profile,
        'properties': properties,
        'owned_properties': owned_properties,
    }
    
    return render(request, 'game/properties.html', context)


@login_required
def travel(request):
    """View for travel."""
    profile = request.user.profile
    
    # Check if player is in jail or hospital
    if profile.is_in_jail:
        messages.error(request, "You are in jail and cannot travel.")
        return redirect('game_home')
    
    if profile.is_in_hospital:
        messages.error(request, "You are in the hospital and cannot travel.")
        return redirect('game_home')
    
    # Get available locations
    locations = Location.objects.all()
    
    context = {
        'profile': profile,
        'locations': locations,
    }
    
    return render(request, 'game/travel.html', context)


@login_required
def gangs(request):
    """View for gangs."""
    profile = request.user.profile
    
    # Get gangs of the player's character type
    gangs = Gang.objects.filter(gang_type=profile.character_type)
    
    # Check if player is in a gang
    try:
        gang_membership = GangMember.objects.get(profile=profile)
        player_gang = gang_membership.gang
        player_role = gang_membership.role
    except GangMember.DoesNotExist:
        player_gang = None
        player_role = None
    
    context = {
        'profile': profile,
        'gangs': gangs,
        'player_gang': player_gang,
        'player_role': player_role,
    }
    
    return render(request, 'game/gangs.html', context)


@login_required
def stock_market(request):
    """View for the stock market."""
    profile = request.user.profile
    
    # Get available stocks
    stocks = StockMarket.objects.all()
    
    # Get owned stocks
    owned_stocks = StockOwnership.objects.filter(profile=profile)
    
    context = {
        'profile': profile,
        'stocks': stocks,
        'owned_stocks': owned_stocks,
    }
    
    return render(request, 'game/stock_market.html', context)


@login_required
def achievements(request):
    """View for achievements."""
    profile = request.user.profile
    
    # Get all achievements
    achievements = Achievement.objects.all()
    
    # Get earned achievements
    earned_achievements = EarnedAchievement.objects.filter(profile=profile)
    earned_achievement_ids = [ea.achievement.id for ea in earned_achievements]
    
    context = {
        'profile': profile,
        'achievements': achievements,
        'earned_achievement_ids': earned_achievement_ids,
    }
    
    return render(request, 'game/achievements.html', context)