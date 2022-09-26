"""
On Mac/Linux:

You can execute this script in the cmd line by executing:
python manage.py shell < mockdatascript.py   

On Windows:
python manage.py shell
exec(open("mockdatascript.py").read())

"""

import datetime
import random
from chewapp.controller.manager import (
    AddCategoryController,
    CreateCouponCodeController,
    CreateNewMenuItemController,
    ModifyCategoryController,
    ViewMenuController,
)

from chewapp.controller.guest import (
    AddToCartController,
    InputTableAndEmailController,
    SubmitCartController,
    ApplyCouponController,
    ModifyCartController,
)

from chewapp.controller.admin import CreateUserProfileController, CreateUsersController
from chewapp.models import OrderItem


# Creating mock data for testing purposes

# Menu Items

CNMIC = CreateNewMenuItemController()
ACC = AddCategoryController()
MCC = ModifyCategoryController()
CCcC = CreateCouponCodeController()
VMC = ViewMenuController()

IETC = InputTableAndEmailController()
ATC = AddToCartController()
SOC = SubmitCartController()
ACc = ApplyCouponController()
MC = ModifyCartController()
CUPC = CreateUserProfileController()
CUC = CreateUsersController()


def date_generator():
    start_date = datetime.datetime(2020, 1, 1).replace(tzinfo=datetime.timezone.utc)
    end_date = datetime.datetime(2022, 5, 27).replace(tzinfo=datetime.timezone.utc)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + datetime.timedelta(days=random_number_of_days)


# Category 1
drink_cat, drink_error = ACC.AddCategory("Drink", "Drink up yum yum", [])

drinks_pog = [
    CNMIC.CreateNewMI(
        "Latte",
        "Latte is a blend of espresso and steamed milk, topped with steamed milk and served in a cup.",
        4.00,
        True,
    ),
    CNMIC.CreateNewMI(
        "Espresso",
        "Espresso is a coffee drink made by forcing a small amount of nearly boiling water under pressure through finely ground coffee beans.",
        2.00,
        True,
    ),
    CNMIC.CreateNewMI(
        "Coffee",
        "Coffee is a brewed drink prepared from roasted coffee beans, which are the seeds of berries from the coffee plant.",
        2.00,
        True,
    ),
    CNMIC.CreateNewMI(
        "Coffee Cake", "Coffee cake is a cake flavored with coffee.", 3.00, True
    ),
    CNMIC.CreateNewMI("Sprite", "We love Cola", 1.00, True),
    CNMIC.CreateNewMI("Coke", "We love Cola", 1.00, True),
    CNMIC.CreateNewMI("Water", "We love Cola", 1.00, True),
    CNMIC.CreateNewMI("Milk", "We love Cola", 1.00, True),
]

drink_ids = list()

for drink, error in drinks_pog:
    if error is not None:
        print(error)
    else:
        drink_ids.append(drink.id)


MCC.ModifyCategory(drink_cat.id, drink_cat.name, drink_cat.description, drink_ids)


# We love our pasta

pasta_cat, pasta_error = ACC.AddCategory("Pasta", "Yummers", [])

pasta_pog = [
    CNMIC.CreateNewMI(
        "Aglio Olio",
        "Spaghetti aglio e olio is a traditional Italian pasta dish from Naples.",
        10,
        True,
    ),
    CNMIC.CreateNewMI(
        "Bolognese", "Bolognese is a sauce made from meat and vegetables.", 8, True
    ),
    CNMIC.CreateNewMI(
        "Carbonara",
        "Carbonara is a pasta dish made with eggs, parmesan cheese, and bacon.",
        12,
        True,
    ),
    CNMIC.CreateNewMI(
        "Lasagna",
        "Lasagna is a pasta dish consisting of a layer of pasta layered with a sauce.",
        14,
        True,
    ),
    CNMIC.CreateNewMI(
        "Ravioli",
        "Ravioli is a dish of thin, nearly cylindrical pasta, filled with meat, cheese, or vegetables.",
        11,
        True,
    ),
    CNMIC.CreateNewMI(
        "Spaghetti",
        "Spaghetti is a type of pasta, consisting of a rolled sheet of unleavened dough.",
        10,
        True,
    ),
]

pasta_ids = list()

for pasta, error in pasta_pog:
    if error is not None:
        print(error)
    else:
        pasta_ids.append(pasta.id)

MCC.ModifyCategory(pasta_cat.id, pasta_cat.name, pasta_cat.description, pasta_ids)

# Category 3
baked_cat, baked_error = ACC.AddCategory("Baked Goods", "Oven is great", [])

baked_pog = [
    CNMIC.CreateNewMI(
        "Baked Potato", "Baked potato is a dish of boiled, mashed potatoes.", 5, True
    ),
    CNMIC.CreateNewMI(
        "Baked Ziti", "Baked ziti is a dish of boiled, mashed ziti.", 4, True
    ),
    CNMIC.CreateNewMI(
        "Baked Beans", "Baked beans is a dish of boiled, mashed beans.", 5, False
    ),
    CNMIC.CreateNewMI(
        "Baked Chicken", "Baked chicken is a dish of boiled, mashed chicken.", 7, True
    ),
    CNMIC.CreateNewMI(
        "Baked Fish", "Baked fish is a dish of boiled, mashed fish.", 9, True
    ),
    CNMIC.CreateNewMI(
        "Baked Ham", "Baked ham is a dish of boiled, mashed ham.", 12, True
    ),
]

baked_ids = list()

for food, error in baked_pog:
    if error is not None:
        print(error)
    else:
        baked_ids.append(food.id)

MCC.ModifyCategory(baked_cat.id, baked_cat.name, baked_cat.description, baked_ids)


# We love our asian dishes

asian_cat, asian_error = ACC.AddCategory("Asian", "weee", [])

asian_pog = [
    CNMIC.CreateNewMI(
        "Beef Noodle Soup",
        "Beef noodle soup is a soup made from beef and vegetables.",
        10,
        True,
    ),
    CNMIC.CreateNewMI(
        "Chicken Noodle Soup",
        "Chicken noodle soup is a soup made from chicken and vegetables.",
        8,
        True,
    ),
    CNMIC.CreateNewMI(
        "Pork Noodle Soup",
        "Pork noodle soup is a soup made from pork and vegetables.",
        12,
        True,
    ),
    CNMIC.CreateNewMI(
        "Shrimp Noodle Soup",
        "Shrimp noodle soup is a soup made from shrimp and vegetables.",
        11,
        True,
    ),
    CNMIC.CreateNewMI(
        "Vegetable Noodle Soup",
        "Vegetable noodle soup is a soup made from vegetables.",
        9,
        True,
    ),
]

asia_ids = list()

for asian, error in asian_pog:
    if error is not None:
        print(error)
    else:
        asia_ids.append(asian.id)

MCC.ModifyCategory(asian_cat.id, asian_cat.name, asian_cat.description, asia_ids)


# We love our american dishes

american_cat, american_error = ACC.AddCategory("American", "Oven is great", [])

american_pog = [
    CNMIC.CreateNewMI("Beef Steak", "Beef steak is a dish of cooked steak.", 10, True),
    CNMIC.CreateNewMI(
        "Chicken Breast", "Chicken breast is a dish of cooked chicken breast.", 8, True
    ),
    CNMIC.CreateNewMI(
        "Pork Chop", "Pork chop is a dish of cooked pork chop.", 12, True
    ),
    CNMIC.CreateNewMI("Shrimp", "Shrimp is a dish of cooked shrimp.", 11, True),
    CNMIC.CreateNewMI("Steak", "Steak is a dish of cooked steak.", 9, True),
]

american_ids = list()

for american, error in american_pog:
    if error is not None:
        print(error)
    else:
        american_ids.append(american.id)

MCC.ModifyCategory(
    american_cat.id, american_cat.name, american_cat.description, american_ids
)


# We love our Japanese dishes
japan_cat, japan_error = ACC.AddCategory("Japanese", "wwwww", [])

japan_pog = [
    CNMIC.CreateNewMI(
        "Sushi",
        "Sushi is a Japanese dish of cooked rice, usually with vegetables, and often eaten with soy sauce.",
        10,
        True,
    ),
    CNMIC.CreateNewMI(
        "Tempura",
        "Tempura is a Japanese dish of cooked rice, usually with vegetables, and often eaten with soy sauce.",
        8,
        True,
    ),
    CNMIC.CreateNewMI(
        "Udon",
        "Udon is a Japanese dish of cooked rice, usually with vegetables, and often eaten with soy sauce.",
        12,
        True,
    ),
    CNMIC.CreateNewMI(
        "Yakitori",
        "Yakitori is a Japanese dish of cooked rice, usually with vegetables, and often eaten with soy sauce.",
        11,
        True,
    ),
]

japan_ids = list()

for japanese, error in japan_pog:
    if error is not None:
        print(error)
    else:
        japan_ids.append(japanese.id)

MCC.ModifyCategory(japan_cat.id, japan_cat.name, japan_cat.description, japan_ids)


# We love our Singaporean dishes
sg_cat, sg_error = ACC.AddCategory("SG", "LOCAL EATS", [])

sg_pog = [
    CNMIC.CreateNewMI(
        "Chicken Rice", "Chicken rice is a dish of cooked chicken and rice.", 10, True
    ),
    CNMIC.CreateNewMI("Noodles", "Noodles is a dish of cooked noodles.", 8, True),
    CNMIC.CreateNewMI("Prawns", "Prawns is a dish of cooked prawns.", 12, True),
]

sg_ids = list()

for sg_love, error in sg_pog:
    if error is not None:
        print(error)
    else:
        sg_ids.append(sg_love.id)

MCC.ModifyCategory(sg_cat.id, sg_cat.name, sg_cat.description, sg_ids)


# We love our dessert

dessert_cat, dessert_error = ACC.AddCategory("Desert", "You won't go dry", [])


dessert_pog = [
    CNMIC.CreateNewMI(
        "Chocolate Cake", "Chocolate cake is a dessert made from chocolate.", 10, True
    ),
    CNMIC.CreateNewMI("Cookie", "Cookie is a dessert made from chocolate.", 8, True),
    CNMIC.CreateNewMI(
        "Ice Cream", "Ice cream is a dessert made from chocolate.", 12, True
    ),
    CNMIC.CreateNewMI("Pie", "Pie is a dessert made from chocolate.", 11, True),
    CNMIC.CreateNewMI("Pudding", "Pudding is a dessert made from chocolate.", 9, True),
]

dessert_ids = list()

for desserts, error in dessert_pog:
    if error is not None:
        print(error)
    else:
        dessert_ids.append(desserts.id)

MCC.ModifyCategory(
    dessert_cat.id, dessert_cat.name, dessert_cat.description, dessert_ids
)


# We love our continents(But this means only food in Europe)

continental_cat, continental_error = ACC.AddCategory(
    "Continental", "You won't find find food from the continents other than Europe", []
)


continental_pog = [
    CNMIC.CreateNewMI(
        "Baked PEsto pasta",
        "Baked pasta that will make you fall in love durian",
        10,
        True,
    ),
    CNMIC.CreateNewMI(
        "Baked Kidney Beans with Alfredo",
        "A dish made of kidney beans and Alfredo sauce, not Alfredo kidney ",
        45,
        True,
    ),
    CNMIC.CreateNewMI(
        "Yorkshire Lamb Patties", "Something that's made of lambs", 12, False
    ),
    CNMIC.CreateNewMI(
        "Chicken and cheese salad", "Salad with cheese and chicken", 11, True
    ),
    CNMIC.CreateNewMI(
        "Peppered Pasta Salad",
        "Pasta with some sald mixed with pepper by Pepper Potts",
        9,
        True,
    ),
    CNMIC.CreateNewMI("Rosemary Chicken", "Rose, Chicken and Mary", 55, True),
    CNMIC.CreateNewMI(
        "Grilled Chicken in MUSTARD sauce",
        "Chicken that's finely grilled with capitalised MUSTARD sauce",
        15,
        True,
    ),
    CNMIC.CreateNewMI(
        "Sheperd's Pie",
        "Sheperd who likes pie so maybe that's the reason for Sheperd in the name",
        24,
        False,
    ),
    CNMIC.CreateNewMI(
        "Coronation chicken", "Probably made of chicken who had corona", 2, True
    ),
    CNMIC.CreateNewMI("Khao Soi", "Don't even know what it is", 100, True),
    CNMIC.CreateNewMI(
        "Baked Vegetables",
        "A dish that you could've just made and at home and saved moni",
        99,
        True,
    ),
]

continental_ids = list()

for continental, error in continental_pog:
    if error is not None:
        print(error)
    else:
        continental_ids.append(continental.id)

MCC.ModifyCategory(
    continental_cat.id,
    continental_cat.name,
    continental_cat.description,
    continental_ids,
)


# Indian food but for some reason is also called Pakistani, Iranian or some other country's dishes

indian_cat, indian_error = ACC.AddCategory(
    "Indian",
    "Food that's filled with spices and will make you sit in the washroom the next day",
    [],
)

indian_pog = [
    CNMIC.CreateNewMI(
        "Biryani",
        "Rice filled with chillies and spices that you can't even place on your tongue",
        8.5,
        True,
    ),
    CNMIC.CreateNewMI(
        "Palak Paneer", "Spinach curry with tofu's twin(paneer) mixed in it", 10, True
    ),
    CNMIC.CreateNewMI(
        "Panner Butter Masala",
        "Indian cottage cheese with Butter and Masala(Mixture of spices)",
        10,
        True,
    ),
    CNMIC.CreateNewMI(
        "Kichidi",
        "A blunt dish that is sold to foreigners by an Indian by exaggerating it",
        5.5,
        False,
    ),
    CNMIC.CreateNewMI(
        "Paani Puri",
        "A dish that will surely make your stomach upset if you aren't an indian",
        13,
        True,
    ),
    CNMIC.CreateNewMI(
        "Samosa", "A dish that's really tasty but the shape looks like poop", 10.5, True
    ),
    CNMIC.CreateNewMI(
        "Kachori",
        "It doesn't look anything like poop but is a famous contender of Samosa",
        10,
        True,
    ),
    CNMIC.CreateNewMI(
        "Naan",
        "A very famous indian bread that turns into rubber within a minute",
        2,
        True,
    ),
    CNMIC.CreateNewMI(
        "Dosa",
        "It's totally different from a pancake but non-indians call it a pancake for some reason",
        4.5,
        False,
    ),
    CNMIC.CreateNewMI(
        "Gulab Jamun",
        "Gulab means rose in english but this dish is nothing like the colot of rose instead is brown in color",
        3.25,
        True,
    ),
    CNMIC.CreateNewMI(
        "Chicken leg piece",
        "For some reason there was a song made on it which went viral in India",
        4.25,
        False,
    ),
]

indian_ids = list()

for indian, error in indian_pog:
    if error is not None:
        print(error)
    else:
        indian_ids.append(indian.id)

MCC.ModifyCategory(indian_cat.id, indian_cat.name, indian_cat.description, indian_ids)


# Pizza - need to be said with a T, peeTza

pizza_cat, pizza_error = ACC.AddCategory(
    "Pizza", "Pizza is the only Italian food we all know or maybe pasta too", []
)

pizza_pog = [
    CNMIC.CreateNewMI(
        "Margerita Pizza",
        "We all rub pizza on our faces when we are home alone just to portray our love for it",
        12.5,
        True,
    ),
    CNMIC.CreateNewMI("Pepperoni Pizza", "Pizza with pepperoni", 12.5, True),
    CNMIC.CreateNewMI("Veggie Pizza", "Pizza with vegetables", 12.5, False),
    CNMIC.CreateNewMI("Hawaiian Pizza", "Pizza with ham and pineapple", 12.5, True),
    CNMIC.CreateNewMI(
        "Meat Lovers Pizza", "Pizza with chicken, beef and bacon", 12.5, True
    ),
    CNMIC.CreateNewMI(
        "Supreme Pizza",
        "Pizza with chicken, beef, bacon, mushrooms and onions",
        12.5,
        True,
    ),
    CNMIC.CreateNewMI(
        "Veggie Supreme Pizza",
        "Pizza with chicken, beef, bacon, mushrooms and onions",
        12.5,
        True,
    ),
    CNMIC.CreateNewMI(
        "Unlimited Pizza",
        "Unlimited because pizza names can just keep going, so let's move on",
        22.5,
        True,
    ),
]

pizza_ids = list()

for peeja, error in pizza_pog:
    if error is not None:
        print(error)
    pizza_ids.append(peeja.id)

MCC.ModifyCategory(pizza_cat.id, pizza_cat.name, pizza_cat.description, pizza_ids)


# Wine - yeah could be added in drinks category, but in all menu's its always WINE that's in a whole separate menu (drink responsibly)

wine_cat, wine_error = ACC.AddCategory("Wine", "WINE(Vine), for fine dine", [])

wine_pog = [
    CNMIC.CreateNewMI("Wine", "Wine that helps you dine fine at nine", 45, True),
    CNMIC.CreateNewMI("Rose Wine", "Rose with wine, Sorry Wine with rose", 45, True),
    CNMIC.CreateNewMI("Sparkling Wine", "Wine that sparkles", 45, False),
    CNMIC.CreateNewMI("Red Wine", "Wine that's blood red", 45, True),
    CNMIC.CreateNewMI("White Wine", "Wine that's white", 45, True),
    CNMIC.CreateNewMI("Dessert Wine", "Wine that has cake in it", 45, True),
    CNMIC.CreateNewMI("Fortified Wine", "Wine that's served in forts", 65, False),
]

wine_ids = list()

for wine, error in wine_pog:
    if error is not None:
        print(error)
    else:
        wine_ids.append(wine.id)

MCC.ModifyCategory(wine_cat.id, wine_cat.name, wine_cat.description, wine_ids)


# Bubble tea - OHHHHHHH YEAHHHH, bubble tea needs it's own catergory too

bbt_cat, bbt_error = ACC.AddCategory("BBT", "This category needs no INTRODUCTION", [])

bbt_pog = [
    CNMIC.CreateNewMI("Milk tea", "Milk tea with tapioca pearls", 3.75, True),
    CNMIC.CreateNewMI("Green tea", "Green tea with tapioca pearls", 3.75, True),
    CNMIC.CreateNewMI("Oolong tea", "Oolong tea with tapioca pearls", 3.75, True),
    CNMIC.CreateNewMI("Black tea", "Black tea with tapioca pearls", 3.75, True),
    CNMIC.CreateNewMI("Pineapple tea", "Pineapple tea with tapioca pearls", 3.75, True),
    CNMIC.CreateNewMI("Mango tea", "Mango tea with tapioca pearls", 3.75, True),
    CNMIC.CreateNewMI(
        "Strawberry tea", "Strawberry tea with tapioca pearls", 3.75, True
    ),
    CNMIC.CreateNewMI(
        "Passion fruit tea", "Passion fruit tea with tapioca pearls", 3.75, True
    ),
    CNMIC.CreateNewMI("Lemon tea", "Lemon tea with tapioca pearls", 3.75, True),
    CNMIC.CreateNewMI("Coconut tea", "Coconut tea with tapioca pearls", 3.75, True),
]

bbt_ids = list()

for bbt, error in bbt_pog:
    if error is not None:
        print(error)
    else:
        bbt_ids.append(bbt.id)

MCC.ModifyCategory(bbt_cat.id, bbt_cat.name, bbt_cat.description, bbt_ids)


# fINALLY tiMe for FOODHACKERz special

fhz_cat, fhz_error = ACC.AddCategory(
    "FHZ", "This is our specialty with some spices of coding", []
)

fhz_pog = [
    CNMIC.CreateNewMI("Java", "Eat it, or JAVA make NOISEEE!!!", 100.95, False),
    CNMIC.CreateNewMI("C++", "Eat it to increment your age by 1", 100.95, False),
    CNMIC.CreateNewMI("Python", "Eat it or a python will bite you...", 100.95, False),
    CNMIC.CreateNewMI(
        "JavaScript",
        "Eat it or JS will torture you",
        100.95,
        False,
    ),
    CNMIC.CreateNewMI(
        "C#", "C-SHARP, a C with that's Sharp and has no ++", 100.95, True
    ),
    CNMIC.CreateNewMI("C", "C that has no sharp or ++", 100.95, False),
    CNMIC.CreateNewMI("PHP", "LOL Who cares", 100.95, True),
    CNMIC.CreateNewMI(
        "Rust",
        "Eat it or you will corrode yourself",
        100.95,
        False,
    ),
    CNMIC.CreateNewMI("Golang", "The language that has a lang after it", 100.95, True),
]

fhz_ids = list()

for food, error in fhz_pog:
    if error is not None:
        print(error)
    else:
        fhz_ids.append(food.id)

MCC.ModifyCategory(fhz_cat.id, fhz_cat.name, fhz_cat.description, fhz_ids)


# Coupon codes for a special experience for the customers
cc_pog = [
    CCcC.CreateCouponCode("STREAMERADRIEL", 10, 0, 5),
    CCcC.CreateCouponCode("BEATEATTHERICE", 15, 0, 8),
    CCcC.CreateCouponCode("INSANECODERFELIX", 0, 3, 10),
    CCcC.CreateCouponCode("MELODICRHYTHM", 0, 4, 15),
    CCcC.CreateCouponCode("NOOBRAHUL", 5, 0, 2),
    CCcC.CreateCouponCode("SULABHTHEHACKER", 20, 0, 25),
    CCcC.CreateCouponCode("COOLHENG", 0, 1, 10),
    CCcC.CreateCouponCode("WXYZ", 0, 5, 15),
]

cc_ids = list()

for code, error in cc_pog:
    if error is not None:
        print(error)
    else:
        cc_ids.append(code.id)

# Modify coupon code
CCcC.CreateCouponCode("NOOBRAHUL", 0, 1, 100)

# Creating User Profiles


RandomProfiles = list()

for i in range(50):
    is_manager = random.randint(0, 10) >= 5
    is_admin = random.randint(0, 10) == 1
    is_staff = random.randint(0, 10) >= 1
    is_owner = random.randint(0, 10) == 1

    profile, error = CUPC.CreateNewUserProfile(
        name="Profile" + str(i),
        manager=is_manager,
        administrator=is_admin,
        staff=is_staff,
        owner=is_owner,
    )

    if error is not None:
        print(error)

    RandomProfiles.append(profile.id)

# Creating random users
for i in range(200):
    CUC.CreateAccount(
        username="USER" + str(i),
        password="USER" + str(i),
        profile_id=random.choice(RandomProfiles),
        email="USER" + str(i) + "@gmail.com",
    )


for i in range(200):

    # Adding customer and their cart items and submitting order
    # 1
    ite_pog = [
        IETC.InputTableAndEmail(1, "adam@gmail.com"),
        IETC.InputTableAndEmail(2, "terry@gmail.com"),
        IETC.InputTableAndEmail(4, "felix@xyz.com"),
        IETC.InputTableAndEmail(6, "adriel@streamer.com"),
        IETC.InputTableAndEmail(4, "wxy@z.com"),
        IETC.InputTableAndEmail(11, "shaun@gmail.com"),
        IETC.InputTableAndEmail(5, "Beatrice@gmail.com"),
        IETC.InputTableAndEmail(2, "rhythm@gmail.com"),
        IETC.InputTableAndEmail(3, "rahul@gmail.com"),
        IETC.InputTableAndEmail(5, "Beatrice@gmail.com"),
        IETC.InputTableAndEmail(3, "rahul@gmail.com"),
    ]

    cart_IDs = list()

    for cart, error in ite_pog:
        if error is not None:
            print(error)
        else:
            cart_IDs.append(cart.id)

    # Payment references
    ref_list = [
        "5266476285912986, Adam Billy, 1/2028, 632",
        "5451447533138653, Hizkia Felix Winata, 11/2022, 346",
        "5485905474192005, Adriel Tan, 4/2027, 397",
        "5570835115330183, Wee Xin Yi, 12/2027, 945",
        "5295818619766957, Shaun Heng, 10/2024, 358",
        "5487975315409825, Beatrice, 3/2026, 914",
        "5450258779920568, Rhythm, 7/2023, 312",
        "5247435775885361, Terry, 4/2028, 764",
        "5582053784874673, Rahul Nahar, 11/2026, 388",
        "5487975315409825, Beatrice, 3/2026, 914",
        "5582053784874673, Rahul Nahar, 11/2026, 388",
    ]

    menu, err = VMC.GetMenuItems()

    coupon_codes = ["STREAMERADRIEL", "COOLHENG", "SULABHTHEHACKER", "INSANECODERFELIX"]

    # Adds items to the cart
    for cartID in cart_IDs:
        for item in range(random.randint(1, 10)):
            menu_item_no = random.randint(1, len(menu))
            for qty in range(random.randint(1, 10)):
                ATC.AddItem(menu_item_no, cartID)
        if random.random() > 0.8:
            random_cc = random.choice(coupon_codes)
            ACc.GetUpdatedPrice(cartID, random_cc)

    # Submitting order
    for j, cart_id in enumerate(cart_IDs):
        order, _ = SOC.SubmitOrder(cart_id, ref_list[j])
        fakeDate = date_generator()
        order.created_at = fakeDate

        order.save()
