from django.core.management.base import BaseCommand
from sellers.models import PricingPlan

class Command(BaseCommand):
    help = 'Set up initial pricing plans'

    def handle(self, *args, **options):
        # Clear existing pricing plans
        PricingPlan.objects.all().delete()
        
        # Create Basic 3x plan
        basic_plan = PricingPlan.objects.create(
            name='basic',
            display_name='Basic 3x',
            description='Perfect for new businesses',
            monthly_price=567.00,
            yearly_price=5440.00,  # 12 months - 20% discount
            cancelled_monthly_price=750.00,  # Original price
            cancelled_yearly_price=9000.00,  # Original yearly price
            is_popular=False,
            is_active=True
        )
        
        # Create Business 4x plan
        business_plan = PricingPlan.objects.create(
            name='business',
            display_name='Business 4x',
            description='Great for growing businesses',
            monthly_price=567.00,
            yearly_price=5440.00,  # 12 months - 20% discount
            cancelled_monthly_price=850.00,  # Original price
            cancelled_yearly_price=10200.00,  # Original yearly price
            is_popular=True,
            is_active=True
        )
        
        # Create Platinum 10x plan
        platinum_plan = PricingPlan.objects.create(
            name='platinum',
            display_name='Platinum 10x',
            description='Best for established enterprises',
            monthly_price=567.00,
            yearly_price=5440.00,  # 12 months - 20% discount
            cancelled_monthly_price=1200.00,  # Original price
            cancelled_yearly_price=14400.00,  # Original yearly price
            is_popular=False,
            is_active=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {PricingPlan.objects.count()} pricing plans:\n'
                f'- {basic_plan.display_name}: ¢{basic_plan.monthly_price}/month (was ¢{basic_plan.cancelled_monthly_price})\n'
                f'- {business_plan.display_name}: ¢{business_plan.monthly_price}/month (was ¢{business_plan.cancelled_monthly_price}) (Popular)\n'
                f'- {platinum_plan.display_name}: ¢{platinum_plan.monthly_price}/month (was ¢{platinum_plan.cancelled_monthly_price})'
            )
        ) 