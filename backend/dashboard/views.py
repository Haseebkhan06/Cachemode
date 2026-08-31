from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class ExistingBusinessForm(forms.Form):
    business_name = forms.CharField(max_length=200, label='Business name')
    location = forms.CharField(max_length=200, label='Location')
    investment_amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label='Investment amount'
    )


class NewBusinessForm(forms.Form):
    business_idea = forms.CharField(max_length=200, label='Business idea')
    location = forms.CharField(max_length=200, label='Location')
    investment_amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label='Investment amount'
    )


def _generate_market_analysis(business_idea, location, investment_amount):
    idea_text = business_idea.strip()
    location_text = location.strip()
    idea_lower = idea_text.lower()

    base_score = sum(ord(ch) for ch in idea_text.lower()) % 100
    demand_score = 64 + (base_score % 22)
    supply_score = 52 + ((base_score + 18) % 25)
    risk_score = max(28, min(85, round((100 - demand_score) * 0.7 + (float(investment_amount) / 1000000) * 8 + 18)))

    if 'coffee' in idea_lower or 'cafe' in idea_lower:
        category = 'Cafe / QSR'
        big_players = ['Cafe Coffee Day', 'Barista', 'Third Wave Coffee']
        local_names = ['Brew & Bean', 'Horizon Cafe', 'Bean Street', 'Morning Roast']
        market_note = 'The coffee and quick-service segment is highly visible in residential and commercial corridors, with strong repeat purchase potential.'
    elif 'gym' in idea_lower or 'fitness' in idea_lower:
        category = 'Fitness / Wellness'
        big_players = ['Cult.fit', 'Gold Gym', 'Anytime Fitness']
        local_names = ['Iron Pulse', 'FitZone', 'Power House', 'LiveFit']
        market_note = 'Demand is strongest near residential housing clusters and office hubs where high-frequency memberships are common.'
    elif 'restaurant' in idea_lower or 'food' in idea_lower:
        category = 'Food / Dining'
        big_players = ['Domino\'s', 'McDonald\'s', 'KFC']
        local_names = ['Local Bites', 'Spice Route', 'City Plate', 'Crave Corner']
        market_note = 'Food demand remains resilient, but category saturation is high in dense urban micro-markets and mall corridors.'
    elif 'cloth' in idea_lower or 'fashion' in idea_lower or 'boutique' in idea_lower:
        category = 'Retail / Fashion'
        big_players = ['FabIndia', 'Max Fashion', 'Reliance Trends']
        local_names = ['Trend Hub', 'Urban Thread', 'Street Vogue', 'Style Lane']
        market_note = 'Fashion retail is driven by footfall, affordability, and repeat seasonal demand; visibility near high-density markets matters most.'
    else:
        category = 'Service / Retail'
        big_players = ['Local Market Leader', 'Regional Chain', 'National Brand']
        local_names = ['City Growth', 'Next Avenue', 'Prime Line', 'Urban Hub']
        market_note = 'The segment shows moderate demand potential, with competition concentrated in areas with strong footfall and local brand familiarity.'

    competitor_rows = [
        {'name': local_names[0], 'distance': '1.2 km', 'share': '18%', 'strength': 'Strong local loyalty and quick delivery', 'market_share_value': 18},
        {'name': local_names[1], 'distance': '2.8 km', 'share': '15%', 'strength': 'Strong pricing and repeat customer base', 'market_share_value': 15},
        {'name': local_names[2], 'distance': '4.1 km', 'share': '11%', 'strength': 'Premium positioning and digital reach', 'market_share_value': 11},
        {'name': local_names[3], 'distance': '5.4 km', 'share': '9%', 'strength': 'Large format store with broad assortment', 'market_share_value': 9},
    ]

    risk_level = 'High' if risk_score >= 70 else 'Medium' if risk_score >= 45 else 'Low'
    opportunity = 'Healthy' if demand_score >= 70 else 'Moderate' if demand_score >= 55 else 'Watchlist'

    return {
        'business_idea': idea_text,
        'location': location_text,
        'investment_amount': float(investment_amount),
        'category': category,
        'market_note': market_note,
        'risk_score': risk_score,
        'risk_level': risk_level,
        'demand_score': demand_score,
        'supply_score': supply_score,
        'opportunity': opportunity,
        'competitor_rows': competitor_rows,
        'big_players': big_players,
        'risk_factors': [
            'Price sensitivity among local customers is high in the first 6–8 months.',
            'Customer acquisition cost may rise if the business is not visibly distinct from nearby operators.',
            'Operating margins can narrow if rent and staff costs increase faster than sales conversion.',
            'Seasonality and local preference shifts can affect repeat demand in the first year.'
        ],
        'recommendations': [
            'Launch with a niche positioning strategy to make the offer clearly different from nearby operators.',
            'Prioritize a location with higher footfall, parking convenience, and visibility before expansion.',
            'Keep fixed monthly costs under control and test demand with a phased rollout.',
            'Use local digital marketing and customer retention programs to improve repeat purchase volume.'
        ],
        'market_summary': (
            f'In and around {location_text}, the {category.lower()} segment shows {opportunity.lower()} demand potential, '
            f'with {len(competitor_rows)} active comparable operators within a 6 km radius and a clear opportunity for differentiation.'
        ),
    }


@login_required(login_url='login')
def dashboard_home(request):
    return render(request, 'dashboard/dashboard.html')


@login_required(login_url='login')
def existing_business_form(request):
    if request.method == 'POST':
        form = ExistingBusinessForm(request.POST)
        if form.is_valid():
            return render(request, 'dashboard/existing_business_result.html', {
                'business_name': form.cleaned_data['business_name'],
                'location': form.cleaned_data['location'],
                'investment_amount': form.cleaned_data['investment_amount'],
            })
    else:
        form = ExistingBusinessForm()

    return render(request, 'dashboard/existing_business_form.html', {'form': form})


@login_required(login_url='login')
def new_business_form(request):
    if request.method == 'POST':
        form = NewBusinessForm(request.POST)
        if form.is_valid():
            analysis = _generate_market_analysis(
                form.cleaned_data['business_idea'],
                form.cleaned_data['location'],
                form.cleaned_data['investment_amount'],
            )
            return render(request, 'dashboard/new_business_result.html', analysis)
    else:
        form = NewBusinessForm()

    return render(request, 'dashboard/new_business_form.html', {'form': form})
