from enum import Enum

class AssetClass(Enum):
    EQUITY = "equity"
    FIXED_INCOME = "fixed_income"
    CASH = "cash"
    COMMODITY = "commodity"
    PROPERTY = "property"
    CURRENCY = "currency"
    OTHER = "other"

class Sector(Enum):
    ENERGY = "energy"
    MATERIALS = "materials"
    INDUSTRIALS = "industrials"
    UTILITIES = "utilities"
    HEALTH_CARE = "health_care"
    FINANCIALS = "financials"
    CONSUMER_DISCRETIONARY = "consumer_discretionary"
    CONSUMER_STAPLES = "consumer_staples"
    INFORMATION_TECHNOLOGY = "information_technology"
    COMMUNICATION_SERVICES = "communication_services"
    REAL_ESTATE = "real_estate"

