import yaml
import paypalrestsdk
import logging
from django.core.management.base import BaseCommand
import os
from django.conf import settings

PLAN = "plan"
PRODUCT = "product"

logger = logging.getLogger(__name__)

myapi = paypalrestsdk.Api({
	"mode": "live",
	"client_id": "ATI4azSRPWJP1KB0EacJVFtrhTQfb4hXutSb7RdIL-ePGOvw0B82qFotONe_OqLqwhpk3tFECEQ3AYFE",
	"client_secret": "EI9l519ifczqQw9WsdvRBlx1MYnYBYvGf24DjKRba-JgNSQHO7udEsgWaCgn3B6JKnfTvi6pi0URCD2D"
	})

BASE_DIR = os.path.join("..", "..", "..", os.path.dirname(__file__))
PRODUCT_CONF_PATH = os.path.join(BASE_DIR, "product.yml")
PLAN_CONF_PATH = os.path.join(BASE_DIR, "plan.yml")

class Command(BaseCommand):

	help = """
	Manages Paypal Plans
	"""

	def add_arguments(self, parser):
		parser.add_argument(
			"--create",
			"-c",
			choices=[PRODUCT, PLAN],
			help="Creates Paypal plan"
			)
		parser.add_argument(
			"--list",
			"-l",
			choices=[PRODUCT, PLAN],
			help="Lists Paypal plans"
			)
	def create_product(self):
		with open(PRODUCT_CONF_PATH, "r") as f:
			data = yaml.load(f)
			ret = myapi.post("v1/catalogs/products", data)
			print(ret)

	def create_plan(self):
		with open(PLAN_CONF_PATH, "r") as f:
			data = yaml.load(f)
			ret = myapi.post("v1/billing/plans", data)
			print(ret)

	def list_product(self):
		ret = myapi.get("v1/catalogs/products")
		print(ret)

	def list_plan(self):
		ret = myapi.get("v1/billing/plans")
		print(ret)

	def create(self, what):
		if what == PRODUCT:
			self.create_product()
		else:
			self.create_plan()

	def list(self, what):
		if what == PRODUCT:
			self.list_product()
		else:
			self.list_plan()


	def handle(self, *args, **options):
		create_what = options.get("create")
		list_what = options.get("list")

		if create_what:
			print(f"Create a {create_what}")
			self.create(create_what)
		elif list_what:
			print(f"List {list_what}")
			self.list(list_what)