# config/business_model_questions.py

QUESTION_DEFS = [
    # --- A. Customer & Market ---

    {
        "id": "q1_customer_type",
        "label": "Who is your primary customer?",
        "options": {
            "Consumers": "customer_consumers",
            "Businesses": "customer_businesses",
            "Government / public sector": "customer_government",
            "Mixed / ecosystem of actors": "customer_mixed",
        },
    },
    {
        "id": "q2_customer_size",
        "label": "Typical customer size?",
        "options": {
            "Individuals / households": "custsize_individual",
            "Small / medium businesses": "custsize_sme",
            "Large corporates": "custsize_corporate",
            "Communities / co-ops": "custsize_community",
        },
    },
    {
        "id": "q3_market_type",
        "label": "How mature is your target market?",
        "options": {
            "Emerging / new category": "market_emerging",
            "Growing / early majority": "market_growing",
            "Mature / saturated": "market_mature",
            "Highly niche / specialised": "market_niche",
        },
    },
    {
        "id": "q4_purchase_frequency",
        "label": "How often do customers buy or use your solution?",
        "options": {
            "One-off / very rarely": "freq_oneoff",
            "Occasional (once or twice a year)": "freq_occasional",
            "Regular (monthly / quarterly)": "freq_regular",
            "Daily / continuous use": "freq_continuous",
        },
    },
    {
        "id": "q5_decision_maker",
        "label": "Who mainly makes the buying decision?",
        "options": {
            "End user": "decider_end_user",
            "Technical / operations manager": "decider_technical",
            "C-level / executives": "decider_executive",
            "Procurement / public tender": "decider_procurement",
        },
    },
    {
        "id": "q6_sales_cycle",
        "label": "Typical sales cycle length?",
        "options": {
            "Instant / same day": "cycle_instant",
            "Days to weeks": "cycle_short",
            "1–3 months": "cycle_medium",
            "3+ months": "cycle_long",
        },
    },

    # --- B. Problem & Value Proposition ---

    {
        "id": "q7_problem_type",
        "label": "What problem do you mainly solve?",
        "options": {
            "Cost reduction": "value_cost_reduction",
            "Risk / compliance": "value_risk_compliance",
            "Convenience / experience": "value_convenience",
            "Revenue growth": "value_revenue_growth",
        },
    },
    {
        "id": "q8_value_delivery",
        "label": "How is value primarily delivered?",
        "options": {
            "Software / digital service": "delivery_digital",
            "Physical product": "delivery_physical",
            "Service / expertise": "delivery_service",
            "Platform connecting parties": "delivery_platform",
        },
    },
    {
        "id": "q9_customisation_level",
        "label": "Degree of customisation per customer?",
        "options": {
            "Fully standardised": "custom_low",
            "Standard with small configuration": "custom_medium",
            "Highly customised per client": "custom_high",
            "Bespoke / project-by-project": "custom_project",
        },
    },
    {
        "id": "q10_outcome_type",
        "label": "What does your solution primarily optimise?",
        "options": {
            "Efficiency / automation": "outcome_efficiency",
            "Insight / decision-making": "outcome_insight",
            "Experience / engagement": "outcome_experience",
            "Reliability / uptime": "outcome_reliability",
        },
    },
    {
        "id": "q11_switching_costs",
        "label": "How hard is it for customers to switch away from you?",
        "options": {
            "Very easy to switch": "switch_low",
            "Some friction": "switch_medium",
            "Hard due to processes / data": "switch_high_process",
            "Hard due to contracts / assets": "switch_high_contract",
        },
    },
    {
        "id": "q12_urgency",
        "label": "How urgent is the problem you solve?",
        "options": {
            "Nice-to-have": "urgency_low",
            "Important but not urgent": "urgency_medium",
            "Painful / urgent": "urgency_high",
            "Mission-critical": "urgency_mission",
        },
    },

    # --- C. Product / Solution Nature ---

    {
        "id": "q13_solution_form",
        "label": "What form does your solution mainly take?",
        "options": {
            "Pure software": "solution_software",
            "Software + hardware": "solution_soft_hard",
            "Hardware-only": "solution_hardware",
            "Service / consulting only": "solution_service_only",
        },
    },
    {
        "id": "q14_physical_complexity",
        "label": "Physical complexity (if hardware is involved)?",
        "visible_if": {  # CONDITIONAL
            "q13_solution_form": ["solution_soft_hard", "solution_hardware"]
        },
        "options": {
            "Simple devices / kits": "hw_simple",
            "Complex systems / machines": "hw_complex",
            "Large infrastructure / plants": "hw_infrastructure",
        },
    },
    {
        "id": "q15_lifecycle",
        "label": "Typical lifecycle of your product/solution?",
        "options": {
            "Short-lived / disposable": "lifecycle_short",
            "Medium (2–5 years)": "lifecycle_medium",
            "Long-term asset": "lifecycle_long",
            "Continuous evolving service": "lifecycle_continuous",
        },
    },
    {
        "id": "q16_dependency_on_install",
        "label": "Does your solution require installation or integration?",
        "options": {
            "None / pure self-serve": "install_none",
            "Light setup / onboarding": "install_light",
            "Complex IT/OT integration": "install_complex",
            "On-site project implementation": "install_onsite",
        },
    },
    {
        "id": "q17_standardisation",
        "label": "How standardised is your delivery?",
        "options": {
            "Fully standardised": "standard_full",
            "Mostly standard with small tweaks": "standard_high",
            "Mixed standard + bespoke": "standard_mixed",
            "Mostly bespoke": "standard_low",
        },
    },

    # --- D. Revenue & Pricing ---

    {
        "id": "q18_revenue_pattern",
        "label": "How do you primarily WANT to earn revenue?",
        "options": {
            "One-off transactions": "rev_oneoff",
            "Recurring subscription": "rev_subscription",
            "Usage-based / pay-per-use": "rev_usage",
            "Performance-based / success fee": "rev_performance",
        },
    },
    {
        "id": "q19_price_point",
        "label": "Typical deal size per customer?",
        "options": {
            "Micro / impulse (< $10)": "price_micro",
            "Low (< $500)": "price_low",
            "Medium ($500–$50k)": "price_medium",
            "High / enterprise ($50k+)": "price_high",
        },
    },
    {
        "id": "q20_payment_timing",
        "label": "When are you usually paid?",
        "options": {
            "Upfront": "pay_upfront",
            "Milestones": "pay_milestone",
            "After delivery / performance": "pay_after",
            "Ongoing (subscription / retainer)": "pay_ongoing",
        },
    },
    {
        "id": "q21_revenue_diversity",
        "label": "How many revenue streams do you envision?",
        "options": {
            "Single core stream": "revstream_single",
            "2–3 related streams": "revstream_few",
            "Many small streams": "revstream_many",
            "Not sure yet": "revstream_unknown",
        },
    },
    {
        "id": "q22_price_sensitivity",
        "label": "How price-sensitive are your customers?",
        "options": {
            "Extremely price-sensitive": "sensitivity_high",
            "Moderately sensitive": "sensitivity_medium",
            "Low sensitivity / focus on value": "sensitivity_low",
            "Highly regulated / tariff-driven": "sensitivity_regulated",
        },
    },
    {
        "id": "q23_financing_needed",
        "label": "Does your model rely on financing or ownership structures?",
        "options": {
            "No, simple sale": "finance_none",
            "Sometimes financing helps": "finance_optional",
            "Yes, core to model (leasing / PPA etc.)": "finance_core",
            "Involves risk/revenue sharing": "finance_riskshare",
        },
    },

    # --- E. Channels & Distribution ---

    {
        "id": "q24_channel_type",
        "label": "Primary way you reach customers?",
        "options": {
            "Purely online": "channel_online",
            "Direct offline (in-person / sales)": "channel_direct_offline",
            "Partners / distributors": "channel_partners",
            "Marketplaces / platforms": "channel_marketplaces",
        },
    },
    {
        "id": "q25_sales_model",
        "label": "How complex is your sales process?",
        "options": {
            "Self-serve / no salespeople": "sales_selfserve",
            "Light-touch inside sales": "sales_inside",
            "Field sales / complex B2B": "sales_field",
            "Tender / RFP-driven": "sales_tender",
        },
    },
    {
        "id": "q26_geography",
        "label": "Initial target geography?",
        "options": {
            "Local / city / region": "geo_local",
            "National": "geo_national",
            "Regional (e.g. SADC, EU)": "geo_regional",
            "Global": "geo_global",
        },
    },
    {
        "id": "q27_distribution_assets",
        "label": "Do you own distribution infrastructure?",
        "options": {
            "No, use existing channels": "dist_asset_light",
            "Some assets (e.g. vehicles, small fleet)": "dist_asset_medium",
            "Heavy assets (warehouses, depots)": "dist_asset_heavy",
            "Purely digital distribution": "dist_digital_only",
        },
    },
    {
        "id": "q28_customer_contact",
        "label": "How often do you interact directly with customers?",
        "options": {
            "Rarely / one-off": "contact_rare",
            "Periodic check-ins": "contact_periodic",
            "Regular / monthly touchpoints": "contact_regular",
            "Continuous engagement": "contact_continuous",
        },
    },

    # --- F. Operations & Assets ---

    {
        "id": "q29_asset_intensity",
        "label": "Asset intensity of your model?",
        "options": {
            "Very asset-light": "asset_light",
            "Moderate assets": "asset_medium",
            "Asset-heavy": "asset_heavy",
            "IP / data is the main asset": "asset_ip_data",
        },
    },
    {
        "id": "q30_operational_complexity",
        "label": "Operational complexity?",
        "options": {
            "Simple, few moving parts": "ops_simple",
            "Moderate coordination": "ops_medium",
            "High complexity / many actors": "ops_complex",
            "Project-based operations": "ops_project",
        },
    },
    {
        "id": "q31_capacity_constraint",
        "label": "What mainly limits your capacity?",
        "options": {
            "People / expertise": "cap_people",
            "Hardware / equipment": "cap_equipment",
            "Cloud / compute": "cap_compute",
            "Regulation / approvals": "cap_regulation",
        },
    },
    {
        "id": "q32_scaling_mode",
        "label": "How do you mainly scale?",
        "options": {
            "Add more people": "scale_people",
            "Add more assets / sites": "scale_assets",
            "Software scales easily": "scale_software",
            "More users / network effects": "scale_network",
        },
    },
    {
        "id": "q33_servicedelivery_model",
        "label": "Service delivery structure?",
        "options": {
            "One-to-one": "delivery_121",
            "One-to-many": "delivery_1many",
            "Many-to-many": "delivery_manymany",
            "Mostly automated": "delivery_automated",
        },
    },

    # --- G. Data & IP ---

    {
        "id": "q34_data_role",
        "label": "Role of data in your model?",
        "options": {
            "Minimal": "data_low",
            "Supports operations": "data_support",
            "Central value driver": "data_core",
            "You sell data / insights": "data_monetised",
        },
    },
    {
        "id": "q35_ai_usage",
        "label": "How do you use AI/ML?",
        "options": {
            "None planned": "ai_none",
            "Internal optimisation only": "ai_internal",
            "Core part of value": "ai_core_value",
            "You sell AI as a service": "ai_sold",
        },
    },
    {
        "id": "q36_ip_strategy",
        "label": "IP posture?",
        "options": {
            "Trade secrets only": "ip_trade_secrets",
            "Trademarks / branding focus": "ip_brand",
            "Patents / registrable IP planned": "ip_patents",
            "Licensing IP to others is key": "ip_licensing_core",
        },
    },
    {
        "id": "q37_lock_in_mechanism",
        "label": "Primary customer lock-in mechanism?",
        "options": {
            "Habit / UX": "lockin_ux",
            "Data / integrations": "lockin_data",
            "Hardware / installed base": "lockin_hardware",
            "Contracts / long-term agreements": "lockin_contracts",
        },
    },
    {
        "id": "q38_openness",
        "label": "How open is your tech/platform?",
        "options": {
            "Closed, proprietary": "open_closed",
            "Partially open (APIs etc.)": "open_partial",
            "Open-core / open-source base": "open_core",
            "Fully open / ecosystem-driven": "open_full",
        },
    },
    {
        "id": "q39_analytics_layer",
        "label": "Do you have an analytics / insight layer?",
        "options": {
            "No / minimal": "analytics_none",
            "Basic reporting": "analytics_basic",
            "Advanced dashboards / insights": "analytics_advanced",
            "Predictive / prescriptive analytics": "analytics_predictive",
        },
    },

    # --- H. Partnerships, Impact & Risk ---

    {
        "id": "q40_partnership_role",
        "label": "Role of partners in your model?",
        "options": {
            "Not critical": "partner_low",
            "Sales / distribution partners": "partner_sales",
            "Delivery / operations partners": "partner_ops",
            "Ecosystem / platform co-creators": "partner_ecosystem",
        },
    },
    {
        "id": "q41_regulation_level",
        "label": "Regulatory environment?",
        "options": {
            "Lightly regulated": "reg_light",
            "Moderately regulated": "reg_medium",
            "Highly regulated (e.g. energy, health, finance)": "reg_high",
            "You help others comply": "reg_compliance_service",
        },
    },
    {
        "id": "q42_impact_focus",
        "label": "Do you have an explicit impact / ESG mandate?",
        "options": {
            "No specific impact focus": "impact_none",
            "Some ESG/impact but secondary": "impact_secondary",
            "Strong impact as core value": "impact_core",
            "Cross-subsidising / inclusive model": "impact_crosssubsidy",
        },
    },
    {
        "id": "q43_risk_sharing",
        "label": "Does your model share risk with customers?",
        "options": {
            "No, fixed pricing": "riskshare_none",
            "Some shared risk (bonuses/penalties)": "riskshare_partial",
            "Mostly performance-based": "riskshare_high",
            "Insurance / guarantees built-in": "riskshare_insurance",
        },
    },
    {
        "id": "q44_funding_source",
        "label": "Main funding source for your end-users’ purchase?",
        "options": {
            "Customer's own budget": "fund_own",
            "Grants / donors / public funds": "fund_donor",
            "Project finance / banks": "fund_finance",
            "Embedded finance through you": "fund_embedded",
        },
    },
    {
        "id": "q45_long_term_vision",
        "label": "Long-term strategic play?",
        "options": {
            "Build & sell product/company": "vision_build_sell",
            "Build platform / ecosystem": "vision_platform",
            "IP / licensing portfolio": "vision_ip_portfolio",
            "Long-term asset owner / operator": "vision_asset_owner",
        },
    },
]

