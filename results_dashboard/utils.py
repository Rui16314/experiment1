from otree.api import *
import json
from django.db.models import Avg, Count, Q
from collections import defaultdict

def get_all_auction_data(session):
    """Collect all auction data from all apps"""
    all_data = []
    
    # Get data from each auction app
    auction_apps = [
        'first_price_auction',
        'repeated_first_price_fixed', 
        'first_price_with_chat',
        'second_price_auction',
        'repeated_second_price_fixed',
        'second_price_with_chat'
    ]
    
    for app in auction_apps:
        try:
            players = session.get_participants()
            for player in players:
                if hasattr(player, app.replace('_', '')):
                    app_player = getattr(player, app.replace('_', ''))
                    for round_data in app_player.in_all_rounds():
                        if round_data.valuation:  # Only include completed rounds
                            all_data.append({
                                'valuation': round_data.valuation,
                                'bid': round_data.bid,
                                'points': round_data.points,
                                'session_type': round_data.session_type,
                                'auction_type': round_data.auction_type,
                                'matching_type': round_data.matching_type,
                                'has_communication': round_data.has_communication,
                                'gender': round_data.participant_gender,
                                'age': round_data.participant_age,
                                'race': round_data.participant_race,
                                'is_winner': round_data.is_winner,
                                'round_number': round_data.round_number
                            })
        except:
            continue
    
    return all_data

def prepare_chart_data(data):
    """Prepare data for the specific charts requested"""
    chart_data = {
        'valuation_distribution': defaultdict(int),
        'valuation_distribution_by_gender': defaultdict(lambda: defaultdict(int)),
        'valuation_distribution_men': defaultdict(int),
        'valuation_distribution_women': defaultdict(int),
        'avg_bid_by_valuation': defaultdict(list),
        'avg_bid_by_gender': defaultdict(list),
        'avg_bid_by_age': defaultdict(list),
        'avg_bid_by_race': defaultdict(list),
    }
    
    # Process data for charts
    for item in data:
        val = item['valuation']
        
        # Valuation distribution (intervals of 5, 10, 20)
        interval_5 = (val // 5) * 5
        interval_10 = (val // 10) * 10
        interval_20 = (val // 20) * 20
        
        chart_data['valuation_distribution'][interval_20] += 1
        
        # By gender
        gender = item['gender'] or 'unknown'
        chart_data['valuation_distribution_by_gender'][gender][interval_20] += 1
        
        if gender.lower() == 'male':
            chart_data['valuation_distribution_men'][interval_20] += 1
        elif gender.lower() == 'female':
            chart_data['valuation_distribution_women'][interval_20] += 1
        
        # Average bid by valuation
        if 30 <= val <= 39:
            chart_data['avg_bid_by_valuation']['30-39'].append(item['bid'])
        elif 40 <= val <= 49:
            chart_data['avg_bid_by_valuation']['40-49'].append(item['bid'])
        elif 50 <= val <= 59:
            chart_data['avg_bid_by_valuation']['50-59'].append(item['bid'])
        # Add more intervals as needed
        
        # Average bid by demographic
        if item['bid'] > 0:  # Only include actual bids
            chart_data['avg_bid_by_gender'][gender].append(item['bid'])
            chart_data['avg_bid_by_age'][item['age']].append(item['bid'])
            chart_data['avg_bid_by_race'][item['race'] or 'unknown'].append(item['bid'])
    
    # Calculate averages
    for key in chart_data['avg_bid_by_valuation']:
        chart_data['avg_bid_by_valuation'][key] = sum(chart_data['avg_bid_by_valuation'][key]) / len(chart_data['avg_bid_by_valuation'][key]) if chart_data['avg_bid_by_valuation'][key] else 0
    
    for key in chart_data['avg_bid_by_gender']:
        chart_data['avg_bid_by_gender'][key] = sum(chart_data['avg_bid_by_gender'][key]) / len(chart_data['avg_bid_by_gender'][key]) if chart_data['avg_bid_by_gender'][key] else 0
    
    for key in chart_data['avg_bid_by_age']:
        chart_data['avg_bid_by_age'][key] = sum(chart_data['avg_bid_by_age'][key]) / len(chart_data['avg_bid_by_age'][key]) if chart_data['avg_bid_by_age'][key] else 0
    
    for key in chart_data['avg_bid_by_race']:
        chart_data['avg_bid_by_race'][key] = sum(chart_data['avg_bid_by_race'][key]) / len(chart_data['avg_bid_by_race'][key]) if chart_data['avg_bid_by_race'][key] else 0
    
    return chart_data
