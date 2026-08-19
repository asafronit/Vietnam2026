const POI_DATA = {
  "hanoi": {
    "id": "hanoi",
    "name": "Hanoi",
    "region": "north",
    "seq": 1,
    "lat": 21.0285,
    "lng": 105.8522,
    "color": "#e6194b",
    "counts": {
      "hotels": 4,
      "must_see": 3,
      "attractions": 1,
      "food": 3,
      "markets": 2,
      "logistics": 1
    },
    "poi": {
      "hotels": [
        {
          "name": "Peridot Grand Luxury Boutique",
          "area": "Hoan Kiem, Old Quarter",
          "what": "A 5-star boutique hotel a few minutes' walk from Hoan Kiem Lake, with a rooftop pool and bar looking over the Old Quarter roofline.",
          "why": "Best rating-to-location ratio of any hotel in the four agent proposals",
          "lat": 21.0330476,
          "lng": 105.8462971,
          "approx": false,
          "sources": [
            "https://www.booking.com/hotel/vn/peridot-grand-amp-spa-by-aira-hoan-kiem1.html",
            "https://guide.michelin.com/en/hotels-stays/hanoi"
          ],
          "tier": 5,
          "tierOfficial": true,
          "priceLow": 80,
          "priceHigh": 137,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "GM Premium Hotel",
          "area": "Hoan Kiem, Old Quarter",
          "what": "A small Indochine-style hotel a short walk from Hoan Kiem Lake, with a rooftop pool and bar and a lobby styled like a private residence rather than a chain hotel.",
          "why": "Markets itself as 5-star and is priced and reviewed like one, but the rating is self-declared rather than issued by a tourism authority",
          "lat": 21.0307612,
          "lng": 105.8481999,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g293924-d24001394-Reviews-GM_Premium_Hotel-Hanoi.html",
            "https://www.agoda.com/gm-premium-hotel_2/hotel/hanoi-vn.html",
            "https://guide.michelin.com/en/hotels-stays/hoan-kiem/gm-premium-hotel-15158"
          ],
          "tier": 5,
          "tierOfficial": false,
          "priceLow": 58,
          "priceHigh": 162,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "La Sinfonia del Rey Hotel & Spa",
          "area": "Hoan Kiem, opposite Hoan Kiem Lake",
          "what": "A neoclassical-styled hotel directly across from Hoan Kiem Lake, with a sky bar and a lake-view restaurant on the upper floors.",
          "why": "Unbeatable lake-front position; guest reviews and marketing describe it as 5-star but third-party listings place it at 4-star, so treat the rating as self-promoted",
          "lat": 21.0311556,
          "lng": 105.8541135,
          "approx": true,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g293924-d17627438-Reviews-La_Sinfonia_del_Rey_Hotel_Spa-Hanoi.html",
            "https://www.booking.com/hotel/vn/la-sinfonia-del-rey-amp-spa.html"
          ],
          "tier": 4,
          "tierOfficial": false,
          "priceLow": 55,
          "priceHigh": 130,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Hanoi La Storia Hotel",
          "area": "Old Quarter, near Hang Ma Street and Dong Xuan Market",
          "what": "An 18-room hotel on a quiet Old Quarter street four minutes' walk from Dong Xuan Market, with soundproofed rooms and an in-room computer in some categories.",
          "why": "Officially rated 3.0-star with a genuine budget price point and strong, if imperfect, reviews",
          "lat": 21.0357127,
          "lng": 105.847721,
          "approx": true,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g293924-d12154091-Reviews-Hanoi_La_Storia_Hotel-Hanoi.html",
            "https://www.traveloka.com/en-en/hotel/vietnam/hanoi-la-storia-hotel--4000000389115"
          ],
          "tier": 3,
          "tierOfficial": true,
          "priceLow": 25,
          "priceHigh": 50,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "must_see": [
        {
          "name": "Hoan Kiem Lake",
          "area": "Hoan Kiem",
          "what": "The lake at the centre of old Hanoi, with a small red bridge to a temple island. Locals walk and exercise around it at first light.",
          "why": "The city organises itself around this lake, and walking it is free",
          "lat": 21.0288313,
          "lng": 105.8525357,
          "approx": false,
          "sources": [
            "https://en.wikipedia.org/wiki/Ho%C3%A0n_Ki%E1%BA%BFm_Lake"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Temple of Literature",
          "area": "Dong Da, Van Mieu street",
          "what": "A walled 2.5-hectare Confucian temple complex founded in 1070, with five courtyards, stone stelae on turtle bases recording centuries of exam graduates, and a wooden hall dedicated to Confucius.",
          "why": "Vietnam's first national university and one of Hanoi's oldest intact historical sites",
          "lat": 21.0287903,
          "lng": 105.8359533,
          "approx": true,
          "sources": [
            "https://en.wikipedia.org/wiki/Temple_of_Literature,_Hanoi"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Hoa Lo Prison Museum",
          "area": "Hoan Kiem, Hoa Lo street",
          "what": "A preserved wing of a French colonial-era prison built in 1896, nicknamed the \"Hanoi Hilton\" by American POWs held there in the 1960s-70s. Exhibits include a guillotine and the cell blocks used to hold Vietnamese independence activists.",
          "why": "A blunt, unfiltered look at both the colonial and American-war periods of Vietnamese history, in the middle of the modern city",
          "lat": 21.0254222,
          "lng": 105.8465093,
          "approx": false,
          "sources": [
            "https://www.lonelyplanet.com/vietnam/hanoi/attractions/hoa-lo-prison-museum/a/poi-sig/1141862/357880"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [
        {
          "name": "Vietnam Museum of Ethnology",
          "area": "Cau Giay, about 8km from the Old Quarter",
          "what": "An open-air and indoor museum on the 54 officially recognised ethnic groups of Vietnam, with full-size reconstructed stilt houses and tombs in the garden and 15,000+ artifacts inside.",
          "why": "The single best introduction to the hill-tribe cultures the trip later passes through in Sapa and Ha Giang",
          "lat": 21.0400774,
          "lng": 105.7988403,
          "approx": false,
          "sources": [
            "https://en.wikipedia.org/wiki/Vietnam_Museum_of_Ethnology"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "food": [
        {
          "name": "Bun Cha Huong Lien",
          "area": "Hai Ba Trung",
          "what": "A plain three-storey shop that has grilled pork patties over charcoal since the 1990s, served in a bowl of broth with noodles and herbs.",
          "why": "Michelin Bib Gourmand, and the dish Hanoi is best known for",
          "lat": 21.0180504,
          "lng": 105.8538843,
          "approx": false,
          "sources": [
            "https://guide.michelin.com/vn/en/ha-noi-municipality/hanoi/restaurants"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "michelin_bib",
          "video": null
        },
        {
          "name": "Cha Ca Thang Long",
          "area": "Old Quarter, Duong Thanh street",
          "what": "A no-frills shop where turmeric-marinated fish is grilled tableside on a charcoal brazier, then finished in a pan with dill and spring onion and served over rice noodles.",
          "why": "Michelin Bib Gourmand and the most consistently recommended cha ca address left in the Old Quarter",
          "lat": 21.033293,
          "lng": 105.8459895,
          "approx": false,
          "sources": [
            "https://guide.michelin.com/us/en/ha-noi/ha-noi_2974158/restaurant/cha-ca-thang-long"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "michelin_bib",
          "video": null
        },
        {
          "name": "Gia",
          "area": "Tay Ho (West Lake)",
          "what": "A small tasting-menu restaurant built around a chef's-table kitchen, serving a set multi-course menu that reworks Vietnamese ingredients in a modern fine-dining format.",
          "why": "One of Vietnam's first Michelin-starred restaurants (awarded 2025, retained 2026), and Hanoi's clearest high-end tasting-menu option",
          "lat": 21.0205027,
          "lng": 105.7639271,
          "approx": true,
          "sources": [
            "https://guide.michelin.com/us/en/article/michelin-guide-ceremony/michelin-guide-vietnam-2026"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "international",
          "signal": "michelin_star",
          "video": null
        }
      ],
      "markets": [
        {
          "name": "Dong Xuan Market",
          "area": "Old Quarter, 600m north of Hoan Kiem Lake",
          "what": "Hanoi's largest covered market, three floors and five linked pavilion halls over 6,500 square metres, selling everything from textiles and household goods to a ground-floor food and produce section.",
          "why": "The working market Hanoians actually shop at, not a tourist-only stall row",
          "lat": 21.0382556,
          "lng": 105.849671,
          "approx": false,
          "sources": [
            "https://en.wikipedia.org/wiki/%C4%90%E1%BB%93ng_Xu%C3%A2n_Market"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Hanoi Weekend Night Market",
          "area": "Old Quarter, Hang Dao / Hang Ngang / Hang Luoc streets",
          "what": "A near-3km stretch of Old Quarter streets closed to traffic on Friday, Saturday and Sunday evenings and filled with clothing and souvenir stalls, street food carts, and impromptu street performances.",
          "why": "Only runs three nights a week, so it is worth timing the Hanoi stay around if the dates line up",
          "lat": 21.0335078,
          "lng": 105.8509571,
          "approx": false,
          "sources": [
            "https://vinpearl.com/en/hanoi-weekend-night-market"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "logistics": [
        {
          "name": "Noi Bai Airport to Old Quarter transfer",
          "area": "Noi Bai International Airport to Hoan Kiem",
          "what": "The airport sits about 27-30km north of the Old Quarter; a metered taxi or pre-booked private transfer takes 30-40 minutes off-peak (up to 90 in traffic) and costs roughly 300,000-350,000 VND, while a Grab typically comes in cheaper at around 240,000-250,000 VND plus tolls.",
          "why": "The first and last transfer of the whole trip, and the one most worth pre-booking to skip the arrivals-hall taxi touts",
          "lat": 21.2188925,
          "lng": 105.8044596,
          "approx": false,
          "sources": [
            "https://eternalarrival.com/grab-at-hanoi-airport-noi-bai/",
            "https://unchartedlens.com/routes/vietnam/hanoi-airport-to-city-transport-comparison/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ]
    }
  },
  "ha-giang": {
    "id": "ha-giang",
    "name": "Ha Giang",
    "region": "north",
    "seq": 2,
    "lat": 22.8278,
    "lng": 104.9839,
    "color": "#f58231",
    "counts": {
      "hotels": 0,
      "must_see": 2,
      "attractions": 2,
      "food": 0,
      "markets": 0,
      "logistics": 0
    },
    "poi": {
      "hotels": [],
      "must_see": [
        {
          "name": "Ma Pi Leng Pass",
          "area": "National Road 4C, between Dong Van and Meo Vac",
          "what": "A 20km stretch of road called the \"Happiness Road\", carved into a sheer limestone cliff face at over 2,000m, hugging the mountainside with a straight drop of hundreds of metres to the turquoise Nho Que River below.",
          "why": "One of Vietnam's \"Four Great Passes\" and the single most photographed stretch of the entire Ha Giang loop",
          "lat": 23.2419571,
          "lng": 105.3979217,
          "approx": true,
          "sources": [
            "https://en.wikipedia.org/wiki/M%C3%A3_P%C3%AD_L%C3%A8ng_Pass"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Lung Cu Flag Tower",
          "area": "Lung Cu commune, Dong Van district",
          "what": "A 34.85m octagonal tower on a peak near Vietnam's northernmost point, flying a red flag with a yellow star that covers 54 square metres, one for each recognised ethnic group. Reached by roughly 280-800 stone steps depending on where you park.",
          "why": "The symbolic \"top of Vietnam\" and a standard end-goal of the loop's northern leg",
          "lat": 23.3634614,
          "lng": 105.3163342,
          "approx": true,
          "sources": [
            "https://en.wikipedia.org/wiki/Lung_Cu_Flag_Tower"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [
        {
          "name": "Ha Giang Loop (self-drive or easy-rider motorbike route)",
          "area": "Circuit from Ha Giang City through Quan Ba, Yen Minh, Dong Van, Meo Vac",
          "what": "A roughly 350-400km loop of mountain roads through the Dong Van Karst Plateau Geopark, ridden over 3-4 days either as the driver (own or rented manual motorbike) or as a passenger behind a local \"easy rider\" guide.",
          "why": "The reason this region is on the route at all — hairpin passes, terraced valleys and H'mong villages are only reachable this way",
          "lat": 22.8372564,
          "lng": 105.01257,
          "approx": true,
          "sources": [
            "https://vietnammotorcycletours.com/ha-giang-loop-vietnams-ultimate-motorbike-adventure"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Du Gia village and waterfall",
          "area": "Du Gia commune, about 70km from Ha Giang City",
          "what": "A Tay ethnic village of wooden stilt houses in a rice-field valley, with a swimmable turquoise-pooled waterfall a short walk away; usually reached only by motorbike or car since there is no direct bus.",
          "why": "The loop's quiet counterpoint to Dong Van/Meo Vac — a slower, greener detour with a place to swim",
          "lat": 22.9329158,
          "lng": 105.2233287,
          "approx": true,
          "sources": [
            "https://www.vietnamcoracle.com/to-day-du-gia-village-independent-review/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "food": [],
      "markets": [],
      "logistics": []
    }
  },
  "sapa": {
    "id": "sapa",
    "name": "Sapa",
    "region": "north",
    "seq": 3,
    "lat": 22.3364,
    "lng": 103.844,
    "color": "#ffe119",
    "counts": {
      "hotels": 1,
      "must_see": 2,
      "attractions": 0,
      "food": 1,
      "markets": 0,
      "logistics": 1
    },
    "poi": {
      "hotels": [
        {
          "name": "Pao's Sapa Leisure Hotel",
          "area": "Sapa town hillside, Muong Hoa Valley view",
          "what": "A 223-room resort built into the hillside with terrace views over the Muong Hoa rice-terrace valley and Fansipan, run by CTX Holdings.",
          "why": "Ranked #3 of 180+ Sapa hotels on Tripadvisor and independently confirmed as officially 5-star; note that several reviewers say the room quality feels closer to a solid 3-star by Western standards, so treat the rating as location- and facility-driven rather than a guarantee of finish quality",
          "lat": 22.3270114,
          "lng": 103.8466396,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g311304-d12786956-Reviews-Pao_s_Sapa_Leisure_Hotel-Sapa_Lao_Cai_Province.html",
            "https://www.trip.com/hotels/sapa-hotel-detail-10540093/pao-s-sapa-leisure-hotel/"
          ],
          "tier": 5,
          "tierOfficial": true,
          "priceLow": 90,
          "priceHigh": 180,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "must_see": [
        {
          "name": "Fansipan cable car and Muong Hoa mountain train",
          "area": "Sun Plaza, Sapa town, to Fansipan summit",
          "what": "A combined mountain train (Sun Plaza to Muong Hoa station) and a 6.3km cable car climbing to near the summit of Fansipan, at 3,143m the highest peak in Indochina, with a pagoda complex at the top station.",
          "why": "The easiest way to stand on the \"Roof of Indochina\" without a multi-day trek, and the combo ticket includes both legs",
          "lat": 22.3218699,
          "lng": 103.7995338,
          "approx": true,
          "sources": [
            "https://junglebosstours.com/explorer/tourism-blog/fansipan-mountain-sapa"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Cat Cat Village",
          "area": "San Sa Ho commune, about 3km from Sapa town",
          "what": "A Black H'mong village at the entrance to the Muong Hoa Valley, founded in the mid-19th century, with three streams meeting at Cat Cat waterfall and two chain footbridges crossing it.",
          "why": "The most accessible ethnic-minority village from Sapa town, walkable in an afternoon",
          "lat": 22.3309642,
          "lng": 103.8340516,
          "approx": false,
          "sources": [
            "https://vinpearl.com/en/cat-cat-village-sapa"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [],
      "food": [
        {
          "name": "Thang Co A Quynh",
          "area": "15 Thach Son Street, Sapa town",
          "what": "A long-running local restaurant serving thang co, the H'mong horse-meat and offal stew simmered with highland herbs, alongside other mountain specialities.",
          "why": "The most consistently recommended address in Sapa for this specific regional dish, with an established following on Tripadvisor and local guides alike",
          "lat": 22.3360931,
          "lng": 103.8445752,
          "approx": true,
          "sources": [
            "https://www.tripadvisor.com/Restaurant_Review-g311304-d12951605-Reviews-Thang_Co_A_Quynh_Restaurant-Sapa_Lao_Cai_Province.html"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "traveler_recommended",
          "video": null
        }
      ],
      "markets": [],
      "logistics": [
        {
          "name": "Hanoi to Sapa transfer options",
          "area": "Hanoi to Sapa town",
          "what": "Two practical ways to cover the roughly 300km/6 hours - an overnight sleeper train from Hanoi to Lao Cai followed by a 45-60 minute shuttle up to Sapa, or a direct day or overnight limousine van/sleeper bus (5.5-6 hours, roughly 300,000-660,000 VND depending on seat class).",
          "why": "The overnight train turns a dead travel day into a night's sleep, but only the van/bus goes door-to-door into Sapa town itself",
          "lat": 22.3399787,
          "lng": 103.8485698,
          "approx": false,
          "sources": [
            "https://a21tours.com/sapa-sleeper-bus-vs-limousine-van",
            "https://visit-sapa.com/en/blog/hanoi-sapa-bus-limousine"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ]
    }
  },
  "ha-long": {
    "id": "ha-long",
    "name": "Ha Long and Cat Ba",
    "region": "north",
    "seq": 4,
    "lat": 20.9099,
    "lng": 107.1839,
    "color": "#3cb44b",
    "counts": {
      "hotels": 0,
      "must_see": 2,
      "attractions": 1,
      "food": 0,
      "markets": 0,
      "logistics": 0
    },
    "poi": {
      "hotels": [],
      "must_see": [
        {
          "name": "Ha Long Bay limestone karsts",
          "area": "Ha Long Bay, Quang Ninh province",
          "what": "Roughly 1,600 limestone islands and karst pillars rising from emerald-green water, many topped with vegetation and containing caves; a UNESCO World Heritage Site since 1994.",
          "why": "The reason this leg of the trip exists — best seen slowly, from the deck of an overnight boat",
          "lat": 20.9084384,
          "lng": 107.0682782,
          "approx": false,
          "sources": [
            "https://whc.unesco.org/en/list/672/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Cat Ba National Park",
          "area": "Central Cat Ba Island",
          "what": "A national park covering most of Cat Ba Island's interior, protecting tropical limestone forest, wetlands and mangroves; part of the joint Ha Long Bay-Cat Ba Archipelago UNESCO World Heritage Site and a UNESCO Biosphere Reserve since 2004.",
          "why": "The forested, trekkable counterpart to the bay's boat-only islands, and home to the critically endangered Cat Ba langur",
          "lat": 20.8063272,
          "lng": 107.0383362,
          "approx": true,
          "sources": [
            "https://en.wikipedia.org/wiki/C%C3%A1t_B%C3%A0_National_Park"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [
        {
          "name": "Trung Trang Cave",
          "area": "Cat Ba National Park, about 20-30 minutes from the port",
          "what": "A 300-metre natural cave carved through a mountain in the middle of Cat Ba's largest valley, with stalactites and stalagmites reachable on a short easy walk.",
          "why": "A quick, low-effort cave stop that fits into a cruise itinerary alongside kayaking, without needing a dedicated caving day",
          "lat": 20.7887703,
          "lng": 106.9974369,
          "approx": true,
          "sources": [
            "https://www.bestpricetravel.com/travel-guide/trung-trang-cave.html",
            "https://www.halongbaycruises.com/travel-guide/explore-cat-ba-island-with-halong-bay-cruises-trung-trang-cave.html"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "food": [],
      "markets": [],
      "logistics": []
    }
  },
  "ninh-binh": {
    "id": "ninh-binh",
    "name": "Ninh Binh",
    "region": "north",
    "seq": 5,
    "lat": 20.2505,
    "lng": 105.9745,
    "color": "#42d4f4",
    "counts": {
      "hotels": 1,
      "must_see": 2,
      "attractions": 2,
      "food": 2,
      "markets": 1,
      "logistics": 2
    },
    "poi": {
      "hotels": [
        {
          "name": "Ninh Binh Legend Hotel",
          "area": "City center",
          "what": "A 260-room hotel in the middle of Ninh Binh city with three swimming pools, an indoor pool, outdoor tennis courts, sauna and gym.",
          "why": "The city-center 5-star option, for a stay closer to restaurants and the train station rather than out among the karsts",
          "lat": 20.2744939,
          "lng": 105.9587265,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g303945-d1761735-Reviews-Ninh_Binh_Legend_Hotel-Ninh_Binh_Ninh_Binh_Province.html",
            "https://www.kayak.com/Ninh-Binh-Hotels-Ninh-Binh-Legend-Hotel.376440.ksp"
          ],
          "tier": 5,
          "tierOfficial": true,
          "priceLow": 58,
          "priceHigh": 120,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "must_see": [
        {
          "name": "Trang An Scenic Landscape Complex",
          "area": "Ninh Hai Commune, Hoa Lu District, ~7km from Ninh Binh city",
          "what": "A UNESCO World Heritage limestone karst landscape toured by rowed sampan along a 3-hour river route that threads through nine natural cave tunnels beneath the cliffs.",
          "why": "The UNESCO-listed core of the whole 'Ha Long Bay on land' comparison, and the reason Ninh Binh is on the itinerary at all",
          "lat": 20.2537827,
          "lng": 105.9005014,
          "approx": false,
          "sources": [
            "https://wherearethosemorgans.com/trang-an-boat-tour/",
            "https://www.getyourguide.com/trang-an-l36900/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Tam Coc boat ride",
          "area": "Van Lam Village, Ninh Hai Commune",
          "what": "A shorter 2-hour sampan ride, often rowed by foot, along the Ngo Dong River between rice paddies and through three limestone tunnels (Hang Ca, Hang Hai, Hang Ba) that give Tam Coc its name.",
          "why": "The classic, more compact counterpart to Trang An - green rice-paddy scenery in the dry season, flooded gold fields at harvest",
          "lat": 20.2163426,
          "lng": 105.937457,
          "approx": true,
          "sources": [
            "https://happytovisit.com/ninh-binh-hoa-lu-mua-cave-and-trang-an-tour-and-boat-ride/",
            "https://junglebosstours.com/explorer/tourism-blog/trang-an-boat-tour"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [
        {
          "name": "Hoa Lu Ancient Capital",
          "area": "Truong Yen Commune, ~10km from Ninh Binh city",
          "what": "The restored temples of Dinh Tien Hoang and Le Dai Hanh, marking the site of Vietnam's 10th-century capital, set inside a ring of limestone mountains.",
          "why": "The historical anchor of the region, and usually combined with Trang An or Mua Cave into one day's route",
          "lat": 20.283483,
          "lng": 105.8995986,
          "approx": false,
          "sources": [
            "https://happytovisit.com/ninh-binh-hoa-lu-bai-dinh-trang-an-and-mua-cave-tour/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Bai Dinh Pagoda",
          "area": "Gia Sinh Commune, ~15km from Ninh Binh city",
          "what": "The largest Buddhist temple complex in Vietnam, spread across a hillside with a giant bronze Buddha, hundreds of Arhat statues along covered corridors, and a bell tower housing one of Asia's largest bronze bells.",
          "why": "A different register from the boat-and-karst circuit - scale and religious architecture rather than nature",
          "lat": 20.2752292,
          "lng": 105.8654697,
          "approx": true,
          "sources": [
            "https://happytovisit.com/ninh-binh-hoa-lu-bai-dinh-trang-an-and-mua-cave-tour/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "food": [
        {
          "name": "Duc De Restaurant",
          "area": "City center, Ninh Binh",
          "what": "A long-running goat-meat restaurant on a main street in Ninh Binh city, serving the mountain goat (de nui) dishes the region is known for - steamed, grilled and in hotpot.",
          "why": "Consistently the most-reviewed goat-meat specialist in the city center, with a reputation built over years rather than a recent tourist spike",
          "lat": 20.2340333,
          "lng": 105.9682771,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Restaurant_Review-g303945-d8853028-Reviews-Duc_De_Restaurant-Ninh_Binh_Ninh_Binh_Province.html"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "traveler_recommended",
          "video": null
        },
        {
          "name": "Trung Tuyet",
          "area": "City center, Ninh Binh",
          "what": "A local eatery specializing in com chay - sun-dried rice pressed into crisp sheets, deep-fried and served with a savory meat-and-mushroom sauce - alongside egg soup and pho.",
          "why": "Ranked among the most reliable all-rounders in Ninh Binh on both Tripadvisor and Lonely Planet for the region's signature souvenir dish",
          "lat": 20.2516139,
          "lng": 105.97874,
          "approx": false,
          "sources": [
            "https://pioneersailtravel.com/ninh-binh-restaurants/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "traveler_recommended",
          "video": null
        }
      ],
      "markets": [
        {
          "name": "Cho Rong (Rong Market)",
          "area": "71 Van Giang Street, Thanh Binh Ward",
          "what": "Ninh Binh city's main traditional market, spread across a three-story building and open-air stalls, selling household goods, textiles and a fresh-produce section with rice, fish, mountain goat meat and Kim Son rice wine.",
          "why": "The everyday market locals actually shop at, as opposed to the tourist-facing night market",
          "lat": 20.2561711,
          "lng": 105.9776166,
          "approx": true,
          "sources": [
            "https://hanoiexploretravel.com/things-to-do-ninh-binh/rong-market"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "logistics": [
        {
          "name": "Ninh Binh to Hanoi (train and road)",
          "area": "Regional transfer",
          "what": "Ninh Binh's train station sits centrally in the city; five daily trains run to Hanoi's main station on Le Duan Street in about 2 hours, or a private car takes roughly the same time by road.",
          "why": "Fixes the practical transfer time between Ninh Binh and the trip's Hanoi anchor",
          "lat": 20.2421142,
          "lng": 105.9746207,
          "approx": false,
          "sources": [
            "https://oxalisadventure.com/hanoi-to-ninh-binh-best-transport-options/",
            "https://a21tours.com/ninh-binh-city-to-hanoi-transfer"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Lotus Train - Ninh Binh to Dong Hoi (night train)",
          "area": "Ninh Binh Railway Station, departure point",
          "what": "A privately refurbished overnight sleeper carriage (2-berth or 4-berth cabins, Vietnam Railways track) departing Ninh Binh around 22:00 and arriving Dong Hoi around 06:00, with onboard wifi, snacks and breakfast.",
          "why": "Turns the long road transfer south toward Phong Nha into a night's sleep instead of a lost travel day",
          "lat": 20.2421142,
          "lng": 105.9746207,
          "approx": false,
          "sources": [
            "https://lotustrain.vn/ninh-binh-to-dong-hoi-lotus-express",
            "https://violetexpresstrain.com/ninh-binh-dong-hoi-on-lotus-train-se19.html"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ]
    }
  },
  "phong-nha": {
    "id": "phong-nha",
    "name": "Phong Nha",
    "region": "central",
    "seq": 6,
    "lat": 17.5934,
    "lng": 106.2865,
    "color": "#4363d8",
    "counts": {
      "hotels": 1,
      "must_see": 1,
      "attractions": 3,
      "food": 0,
      "markets": 0,
      "logistics": 0
    },
    "poi": {
      "hotels": [
        {
          "name": "Phong Nha Farmstay",
          "area": "Cu Nam, ~10km from Phong Nha town",
          "what": "The original farmstay of the area — simple rooms and a pool set among rice fields and grazing buffalo, run by an Australian-Vietnamese family with a restaurant and tour desk on site.",
          "why": "TripAdvisor's #1-ranked property in the national park (1,500+ reviews) and one of the two hotels the project's own agents agreed on.",
          "lat": 17.5818037,
          "lng": 106.3087403,
          "approx": true,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g4014591-d1930272-Reviews-Phong_Nha_Farmstay-Phong_Nha_Ke_Bang_National_Park_Quang_Binh_Province.html",
            "https://www.booking.com/hotel/vn/phong-nha-farmstay.html"
          ],
          "tier": 3,
          "tierOfficial": false,
          "priceLow": 14,
          "priceHigh": 34,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "must_see": [
        {
          "name": "Paradise Cave",
          "area": "Phong Nha-Ke Bang National Park",
          "what": "A dry cave reached by a steep staircase and jungle path, then a kilometre of wooden walkway through a cavern hung with stalactites lit to look like an underground cathedral.",
          "why": "Regularly named one of the most beautiful caves in Vietnam, and doable without a guide or booking ahead",
          "lat": 17.5192008,
          "lng": 106.223045,
          "approx": true,
          "sources": [
            "https://www.vietnamtourism.com/en/phong-nha-ke-bang-national-park-tickets-complete-2026-price-guide-and-cave-selection-2",
            "https://oxalisadventure.com/paradise-cave-in-phong-nha/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [
        {
          "name": "Dark Cave zipline and mud bath",
          "area": "Chay River, Phong Nha-Ke Bang National Park",
          "what": "A short zipline across the Chay River into a pitch-black cave, followed by a swim to a natural mud pool deep inside, then kayaking back down the river.",
          "why": "The easiest adrenaline activity in Phong Nha — half a day, no fitness test, and the one every family and backpacker group does",
          "lat": 17.5742556,
          "lng": 106.2527864,
          "approx": true,
          "sources": [
            "https://www.getyourguide.com/phong-nha-l176859/phong-nha-cave-exploration-and-zipline-dark-cave-tour-t511831/",
            "https://junglebosstours.com/explorer/tourism-blog/dark-cave-phong-nha"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "The Duck Stop",
          "area": "Bong Lai Valley, ~10km from Phong Nha town",
          "what": "A small working duck farm where visitors feed and walk a flock of ducks along the paddy dikes, with a buffalo ride and a drink included.",
          "why": "TripAdvisor's #1-ranked Phong Nha attraction and the easiest, lightest thing to do on a rest day between caves",
          "lat": 17.6041976,
          "lng": 106.3657674,
          "approx": true,
          "sources": [
            "https://theduckstop.vn/",
            "https://culturephamtravel.com/the-duck-stop/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Pub with Cold Beer",
          "area": "Bong Lai Valley, near the Rao Con River",
          "what": "A rustic family farm-bar down a country lane where you pick a live chicken from the garden and it's grilled to order, eaten in hammocks by the river.",
          "why": "The best-known stop on the Bong Lai Valley motorbike loop and a genuinely local, unstaged meal",
          "lat": 17.5982371,
          "lng": 106.3635278,
          "approx": true,
          "sources": [
            "https://culturephamtravel.com/the-duck-stop/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "food": [],
      "markets": [],
      "logistics": []
    }
  },
  "hue": {
    "id": "hue",
    "name": "Hue",
    "region": "central",
    "seq": 7,
    "lat": 16.4637,
    "lng": 107.5909,
    "color": "#911eb4",
    "counts": {
      "hotels": 4,
      "must_see": 1,
      "attractions": 1,
      "food": 2,
      "markets": 1,
      "logistics": 1
    },
    "poi": {
      "hotels": [
        {
          "name": "Meliá Vinpearl Hue",
          "area": "City center, near the Perfume River and Truong Tien Bridge",
          "what": "A high-rise 5-star hotel in the middle of Hue with a full-service spa, indoor pool, gym and sauna, a 10-minute walk from the Perfume River and Truong Tien Bridge.",
          "why": "The master-spec's own pick for a restored Hue visit, and the highest-reviewed international-chain 5-star in the city (9.4/10 from over 3,000 reviews)",
          "lat": 16.463231,
          "lng": 107.5941414,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g293926-d15113220-Reviews-Melia_Vinpearl_Hue-Hue_Thua_Thien_Hue_Province.html",
            "https://www.melia.com/en/hotels/vietnam/hue-city/melia-vinpearl-hue"
          ],
          "tier": 5,
          "tierOfficial": true,
          "priceLow": 54,
          "priceHigh": 200,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Eldora Hotel",
          "area": "City center",
          "what": "An 81-room boutique hotel with bright, wood-floored rooms in a renaissance-style building in central Hue.",
          "why": "One of the few hotels in Hue with an unambiguous official 4-star classification rather than a self-declared one, and consistently praised for cleanliness",
          "lat": 16.4648595,
          "lng": 107.5945502,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g293926-d6416461-Reviews-Eldora_Hotel-Hue_Thua_Thien_Hue_Province.html",
            "https://www.kayak.com/Hue-Hotels-Eldora-Hotel.2076224.ksp"
          ],
          "tier": 4,
          "tierOfficial": true,
          "priceLow": 35,
          "priceHigh": 90,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Jade Scene Hotel",
          "area": "30/42 Nguyen Cong Tru Street, near the pub street and Perfume River embankment",
          "what": "A new hotel a short walk from Hue's pub street and the river embankment, with a small rooftop pool overlooking the city and a spa.",
          "why": "One of the highest-rated hotels of any tier in Hue (9.2/10 from over 3,000 reviews) and an officially assessed 3-star, not a self-rated boutique",
          "lat": 16.4695305,
          "lng": 107.5968967,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g293926-d25179951-Reviews-Jade_Scene_Hotel-Hue_Thua_Thien_Hue_Province.html",
            "https://www.booking.com/hotel/vn/jade-scene.html"
          ],
          "tier": 3,
          "tierOfficial": true,
          "priceLow": 33,
          "priceHigh": 100,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Thanh Lich Hue Hotel",
          "area": "City center",
          "what": "A 40-room hotel with air-conditioned rooms, minibars and an indoor pool and sauna, with a rooftop breakfast serving both Asian and Western options.",
          "why": "A dependable budget-friendly city-center option (9.0/10 from over 900 reviews), though its 'plus' star billing is self-declared",
          "lat": 16.4703117,
          "lng": 107.5959428,
          "approx": false,
          "sources": [
            "https://www.momondo.com/hotels/hue/Thanh-Lich-Hue-Hotel.mhd2207716.ksp",
            "https://www.kayak.com/Hue-Hotels-Thanh-Lich-2-Hotel.2207716.ksp"
          ],
          "tier": 3,
          "tierOfficial": false,
          "priceLow": 25,
          "priceHigh": 54,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "must_see": [
        {
          "name": "Khai Dinh Tomb",
          "area": "Chau Chu Village, ~10km from Hue city",
          "what": "The last and most ornate of the Nguyen royal tombs, its concrete exterior built in a Gothic-tinged European style but its interior sarcophagus chamber an explosion of colorful ceramic-mosaic murals, reached by 127 stone steps.",
          "why": "The most visually striking of the seven royal tombs and unlike any other Nguyen monument in Hue",
          "lat": 16.3989537,
          "lng": 107.5902801,
          "approx": false,
          "sources": [
            "https://vinwonders.com/en/wonderpedia/news/khai-dinh-tomb-things-to-know-about-the-last-imperial-tomb-built-in-hue/",
            "https://www.lonelyplanet.com/vietnam/central-vietnam/hue/attractions/tomb-of-khai-dinh/a/poi-sig/1158037/357875"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [
        {
          "name": "Tu Duc Tomb",
          "area": "Thuy Xuan Village, ~7km from Hue city",
          "what": "A landscaped royal retreat built around a lake in a pine-forested valley, where Emperor Tu Duc lived, wrote poetry and boated for years before his death, dotted with pavilions and temples rather than a single mausoleum building.",
          "why": "The gentlest and most park-like of the tombs - built as a living retreat, not just a burial site - and a contrast to Khai Dinh's grandeur",
          "lat": 16.433089,
          "lng": 107.5647017,
          "approx": false,
          "sources": [
            "https://centralvietnamguide.com/tu-duc-tomb/",
            "https://vinpearl.com/en/tu-duc-tomb-one-of-the-most-appealing-attractions-in-hue-to-visit"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "food": [
        {
          "name": "Bun Bo Hue Ba Gai",
          "area": "11A Ha Noi Street, Vinh Ninh",
          "what": "A 24-hour noodle shop serving bun bo Hue, the city's own spicy lemongrass-and-beef broth noodle soup, in a plain no-frills dining room popular with locals at all hours.",
          "why": "One of the most consistently recommended bun bo Hue spots in the city that actually invented the dish, open around the clock",
          "lat": 16.4639321,
          "lng": 107.5863388,
          "approx": true,
          "sources": [
            "https://www.willflyforfood.net/hue-food-guide/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "traveler_recommended",
          "video": null
        },
        {
          "name": "Lac Thien (Banh Khoai Lac Thien)",
          "area": "6 Dinh Tien Hoang Street",
          "what": "A family-run restaurant grilling banh khoai to order - Hue's crisp turmeric rice-flour pancake, folded over pork, shrimp and bean sprouts and eaten wrapped in rice paper with a thick peanut-sesame dipping sauce.",
          "why": "Widely cited as Hue's best banh khoai, and the crunchiest version of the dish in the city",
          "lat": 16.4720712,
          "lng": 107.5846611,
          "approx": true,
          "sources": [
            "https://beebeetravel.com/banh-khoai-lac-thien-hue-local-food/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "traveler_recommended",
          "video": null
        }
      ],
      "markets": [
        {
          "name": "Dong Ba Market",
          "area": "North bank of the Perfume River, city center",
          "what": "Hue's biggest market, a three-floor bell-shaped building where the ground floor sells dried seafood and local sauces, the second floor sells crafts like forged knives and ceramics, and the third is devoted to ao dai tailoring.",
          "why": "Central Vietnam's largest and oldest market, and as much a symbol of Hue's identity as the Citadel",
          "lat": 16.4724474,
          "lng": 107.5886452,
          "approx": false,
          "sources": [
            "https://vinwonders.com/en/wonderpedia/news/dong-ba-market-take-a-tour-to-one-of-the-busiest-markets-in-hue/",
            "https://vietnamdiscovery.com/hue/shopping/dong-ba-market/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "logistics": [
        {
          "name": "Phu Bai Airport to Hue city center",
          "area": "Airport transfer",
          "what": "Phu Bai International Airport sits about 15km south of Hue; a taxi or private car to the city center takes 20-30 minutes and costs roughly 250,000-300,000 VND ($10-12).",
          "why": "Fixes the transfer time for flying in or out of Hue directly, rather than via Da Nang",
          "lat": 16.399655,
          "lng": 107.7054596,
          "approx": false,
          "sources": [
            "https://www.geckoroutes.com/vietnam/hue-airport/",
            "https://danangtransfer.vn/en/4-ways-to-get-from-hue-airport-to-city-center-price-time-tips/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ]
    }
  },
  "hoi-an": {
    "id": "hoi-an",
    "name": "Hoi An and Da Nang",
    "region": "central",
    "seq": 8,
    "lat": 15.8801,
    "lng": 108.338,
    "color": "#f032e6",
    "counts": {
      "hotels": 4,
      "must_see": 2,
      "attractions": 2,
      "food": 4,
      "markets": 0,
      "logistics": 2
    },
    "poi": {
      "hotels": [
        {
          "name": "Silkotel Hoi An",
          "area": "Cam Pho Ward, close to Old Town",
          "what": "A mid-size hotel with an outdoor pool, spa, gym and restaurant a short walk from the Old Town's riverside streets.",
          "why": "The master-spec's 'best value' pick for Hoi An, rated 9.1/10 from 1,700 reviews at roughly two-thirds the price of the resort-style 5-stars",
          "lat": 15.8794893,
          "lng": 108.3223668,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g298082-d10259528-Reviews-Silkotel_Hoi_An-Hoi_An_Quang_Nam_Province.html",
            "https://www.hotelscombined.com/Hotel/Silkotel_Hoi_An.htm"
          ],
          "tier": 4,
          "tierOfficial": true,
          "priceLow": 41,
          "priceHigh": 91,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Lasenta Boutique Hotel Hoian",
          "area": "Edge of town, among rice fields",
          "what": "A boutique hotel on the edge of Hoi An with an infinity pool and 4th-floor bar looking out over open rice paddies, plus a free shuttle to both Old Town and the beach.",
          "why": "Master-spec's alternative pick for the rice-field-view infinity pool at a lower price point than La Siesta",
          "lat": 15.8819958,
          "lng": 108.3403954,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g298082-d10149768-Reviews-Lasenta_Boutique_Hotel_Hoian-Hoi_An_Quang_Nam_Province.html",
            "https://www.vietnamcoracle.com/lasenta-boutique-hotel-hoi-an/"
          ],
          "tier": 4,
          "tierOfficial": true,
          "priceLow": 52,
          "priceHigh": 120,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Hoian Central Hotel",
          "area": "In the heart of Hoi An, steps from the riverside",
          "what": "A small hotel right in the town center with an outdoor pool and free bicycle rental, close enough to the Old Town's riverside streets to walk everywhere.",
          "why": "One of the best-located officially-rated 3-star hotels in town, with ratings above many pricier properties",
          "lat": 15.8797503,
          "lng": 108.319306,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g298082-d13737482-Reviews-Hoian_Central_Hotel-Hoi_An_Quang_Nam_Province.html",
            "https://www.klook.com/hotels/detail/113919-hoian-central-hotel/"
          ],
          "tier": 3,
          "tierOfficial": true,
          "priceLow": 30,
          "priceHigh": 69,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Little Town Villa",
          "area": "Near Hoi An Market, 5 minutes' walk from the Japanese Covered Bridge",
          "what": "A small villa-style property near the town market with a spa, outdoor pool and restaurant, five minutes' walk from the Japanese Covered Bridge.",
          "why": "Rated 5/5 on Tripadvisor from hundreds of reviews despite its official 3-star classification - well above its price bracket",
          "lat": 15.8826344,
          "lng": 108.3244197,
          "approx": true,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g298082-d12192622-Reviews-Little_Town_Villas-Hoi_An_Quang_Nam_Province.html",
            "https://www.booking.com/hotel/vn/little-town-villa.html"
          ],
          "tier": 3,
          "tierOfficial": true,
          "priceLow": 25,
          "priceHigh": 130,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "must_see": [
        {
          "name": "Hoi An Ancient Town and Japanese Covered Bridge",
          "area": "Old Town, along the Thu Bon River",
          "what": "A UNESCO-listed trading-port town of yellow-walled shophouses, Chinese assembly halls and merchant homes dating to the 16th-18th centuries, centred on the 18-metre wooden Japanese Covered Bridge that doubles as a small temple.",
          "why": "The reason Hoi An exists on any itinerary - one of Southeast Asia's best-preserved trading ports, UNESCO-listed since 1999",
          "lat": 15.8779509,
          "lng": 108.3239898,
          "approx": false,
          "sources": [
            "https://vinpearl.com/en/japanese-bridge-hoi-an-a-cultural-symbol-of-the-ancient-town",
            "https://grooviet.com/destination/japanese-covered-bridge/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Ba Na Hills and Golden Bridge",
          "area": "Ba Na Mountain, ~45 minutes west of Da Nang",
          "what": "A hilltop resort reached by a record-length cable car, built around a recreated French hill-station village and the Golden Bridge - a walkway held up by two giant stone hands emerging from the hillside.",
          "why": "The consensus pick over My Son among the trip's competing proposals (route decision R6), and Central Vietnam's most photographed modern landmark",
          "lat": 16.0258471,
          "lng": 108.0362621,
          "approx": true,
          "sources": [
            "https://hoiandaytrip.com/ba-na-hills-tickets/",
            "https://happytovisit.com/golden-bridge-ba-na-hills-marble-mountain-monkey-mountain/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [
        {
          "name": "Marble Mountains (Ngu Hanh Son)",
          "area": "Between Da Nang and Hoi An, on the coast road",
          "what": "Five limestone-and-marble hills, each named for one of the five elements, honeycombed with caves and grottoes containing Buddhist shrines; an elevator and stairs lead up to viewpoints and the Huyen Khong cave, once used as a wartime field hospital.",
          "why": "A genuinely different landscape from Hoi An's flat riverside town, and an easy stop on the way to or from Da Nang",
          "lat": 16.00402,
          "lng": 108.2627745,
          "approx": false,
          "sources": [
            "https://happytovisit.com/golden-bridge-ba-na-hills-marble-mountain-monkey-mountain/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "An Bang Beach surf lesson",
          "area": "An Bang Beach, ~3km east of Old Town",
          "what": "A stretch of sandy beach with gentle, beginner-friendly waves, where expat-run surf schools rent boards and run lessons; the surf season runs roughly September to March.",
          "why": "Hoi An's real board-sport option, and a 20-minute bike ride from the Old Town through rice paddies",
          "lat": 15.9141779,
          "lng": 108.3396551,
          "approx": false,
          "sources": [
            "https://thesurfatlas.com/vietnam-surf/hoi-an-surf/",
            "https://thedeckhousevietnam.com/water-sports/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "food": [
        {
          "name": "Banh Mi Phuong",
          "area": "2B Phan Chu Trinh Street, Old Town",
          "what": "A perpetually busy banh mi stand grilling and assembling its own pork, pate and pickled vegetables into a crusty baguette sandwich to order.",
          "why": "The banh mi Anthony Bourdain called possibly the best in Vietnam - still packed with a line out the door years later",
          "lat": 15.8784841,
          "lng": 108.3320081,
          "approx": true,
          "sources": [
            "https://www.tripadvisor.com/Restaurant_Review-g298082-d2365673-Reviews-Banh_My_Phu_ng-Hoi_An_Quang_Nam_Province.html",
            "https://hiddenhoian.com/eat/banh-mi-phuong-hoi-ans-best-banh-mi/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "traveler_recommended",
          "video": null
        },
        {
          "name": "White Rose Restaurant",
          "area": "533 Hai Ba Trung Street",
          "what": "The restaurant most associated with white rose dumplings (banh bao vac) - translucent rice-dough parcels of spiced minced shrimp, steamed and shaped to resemble a folded rose, then topped with crispy fried shallots.",
          "why": "The dish comes from one family recipe distributed to eateries around town, and this restaurant is the most famous outlet for it",
          "lat": 15.8829593,
          "lng": 108.3250054,
          "approx": false,
          "sources": [
            "https://culturephamtravel.com/white-rose-dumplings-hoi-an/",
            "https://cavinteo.blogspot.com/2024/10/white-rose-restaurant-dumplings-hoi-an-vietnam.html"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "traveler_recommended",
          "video": null
        },
        {
          "name": "La Maison 1888",
          "area": "InterContinental Danang Sun Peninsula Resort, Son Tra",
          "what": "A fine-dining French restaurant inside a recreated Indochinese colonial mansion overlooking the sea, serving a five- or eight-course set menu built on Vietnamese, French and Japanese ingredients.",
          "why": "The only Michelin-starred restaurant in Central Vietnam, held by chef Christian Le Squer, who carried three Michelin stars in France for 23 years",
          "lat": 15.9040037,
          "lng": 108.3326237,
          "approx": true,
          "sources": [
            "https://guide.michelin.com/us/en/da-nang-region/da-nang_2984390/restaurant/la-maison-1888",
            "https://www.danang.intercontinental.com/a-michelin-star-for-la-maison-1888/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "international",
          "signal": "michelin_star",
          "video": null
        },
        {
          "name": "Phu Hong (Bun Thit Nuong Phu Hong)",
          "area": "19 Yen Bai Street, Hai Chau District, Da Nang",
          "what": "A street-food stall serving bun thit nuong - grilled pork over rice vermicelli with fresh herbs - alongside grilled pork and minced-pork skewers wrapped in rice paper, no reservations, cash only.",
          "why": "Holds a Michelin Bib Gourmand for good quality, good value cooking - the everyday-food end of Da Nang's Michelin coverage, distinct from La Maison 1888's fine dining",
          "lat": 16.0695853,
          "lng": 108.2229138,
          "approx": true,
          "sources": [
            "https://liveyounglivewell.com/quan-phu-hong-da-nang-review/",
            "https://guide.michelin.com/en/da-nang-region/da-nang_2984390/restaurant/phu-hong"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "michelin_bib",
          "video": null
        }
      ],
      "markets": [],
      "logistics": [
        {
          "name": "Da Nang Airport to Hoi An",
          "area": "Airport transfer",
          "what": "Da Nang International Airport (DAD) sits about 30km from Hoi An; a Grab car or taxi takes 30-40 minutes in normal traffic (up to an hour at peak times) and costs roughly 250,000-400,000 VND.",
          "why": "Fixes the practical transfer time for the flight in and out of the Hoi An/Da Nang leg of the trip",
          "lat": 16.0425792,
          "lng": 108.1971613,
          "approx": false,
          "sources": [
            "https://unmappedasia.com/da-nang-airport-to-hoi-an/",
            "https://www.welcomepickups.com/da-nang/airport-to-hoi-an/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Hoi An Old Town vehicle restrictions",
          "area": "Old Town core",
          "what": "Cars and, at scheduled hours, motorbikes are barred from the Old Town's core streets, which are walking- and cyclo-only; a paid Old Town ticket covers entry to several assembly halls, temples and heritage houses.",
          "why": "Affects how you actually move around and reach hotels/restaurants once inside the historic core",
          "lat": 15.8779509,
          "lng": 108.3239898,
          "approx": false,
          "sources": [
            "https://grooviet.com/destination/japanese-covered-bridge/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ]
    }
  },
  "buon-ma-thuot": {
    "id": "buon-ma-thuot",
    "name": "Buon Ma Thuot",
    "region": "highlands",
    "seq": 9,
    "lat": 12.6797,
    "lng": 108.0378,
    "color": "#9a6324",
    "counts": {
      "hotels": 1,
      "must_see": 3,
      "attractions": 0,
      "food": 0,
      "markets": 1,
      "logistics": 1
    },
    "poi": {
      "hotels": [
        {
          "name": "Dakruco Hotel",
          "area": "City center",
          "what": "A long-running business hotel in central Buon Ma Thuot, run by the state-owned Dak Lak Rubber company, with an outdoor pool, restaurant and bar.",
          "why": "The cheapest hotel in the centre with a genuinely high review score rather than an inflated one",
          "lat": 12.6933774,
          "lng": 108.0660931,
          "approx": true,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g670918-d1772273-Reviews-Dakruco_Hotel-Buon_Ma_Thuot_Dak_Lak_Province.html",
            "https://www.momondo.com/hotels/buon-ma-thuot/Dakruco-Hotel.mhd373818.ksp"
          ],
          "tier": 3,
          "tierOfficial": false,
          "priceLow": 28,
          "priceHigh": 38,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "must_see": [
        {
          "name": "The World Coffee Museum",
          "area": "Tan Loi Ward, inside Trung Nguyen Coffee Village, ~4km from center",
          "what": "A museum built in the style of Central Highlands longhouses, holding over 10,000 coffee-related artefacts from around the world, with hands-on tasting rooms rather than glass display cases.",
          "why": "The signature sight of Vietnam's coffee capital, and the reason most visitors come to Buon Ma Thuot at all",
          "lat": 12.6908584,
          "lng": 108.0445203,
          "approx": false,
          "sources": [
            "https://en.wikipedia.org/wiki/The_World_Coffee_Museum",
            "https://vietnamtourism.gov.vn/en/post/20640"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Ako Dhong Village",
          "area": "Tan Loi Ward, inside the city",
          "what": "A working Ede ethnic-minority neighbourhood inside the city itself, with more than 30 traditional wooden longhouses built on stilts in the shape of boats.",
          "why": "The only place to see genuine Ede stilt-house architecture without leaving town",
          "lat": 12.696465,
          "lng": 108.0491334,
          "approx": false,
          "sources": [
            "https://en.nhandan.vn/ako-dhong-village-a-door-to-explore-ede-ethnic-culture-in-the-heart-of-buon-ma-thuot-city-post146489.html",
            "https://sayhellovietnam.com/ako-dhong-village-an-attractive-village-in-the-city-in-buon-ma-thuot/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Dray Nur Waterfall",
          "area": "Krong Ana district, ~27km southwest of center",
          "what": "A 250-metre-wide waterfall dropping more than 30 metres where the Krong Ana and Krong No rivers meet to form the Serepok River, crossed by a suspension bridge over the gorge.",
          "why": "The most powerful waterfall in the Central Highlands, and a straightforward half-day trip from the city",
          "lat": 12.5405291,
          "lng": 107.8904044,
          "approx": true,
          "sources": [
            "https://vinpearl.com/en/dray-nur-waterfall-dak-lak-things-to-do-here",
            "https://www.tripadvisor.com/Attraction_Review-g670918-d4766576-Reviews-Dray_Nur_Waterfall-Buon_Ma_Thuot_Dak_Lak_Province.html"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [],
      "food": [],
      "markets": [
        {
          "name": "Buon Ma Thuot Central Market",
          "area": "City center, near Victory Monument",
          "what": "The city's main covered market, stalls piled with roasted and green coffee beans, black pepper, cacao, macadamia nuts and honey harvested from the surrounding highland forests.",
          "why": "The place to buy coffee straight from the source rather than at inflated airport prices",
          "lat": 12.6805026,
          "lng": 108.042465,
          "approx": false,
          "sources": [
            "https://www.frommers.com/destinations/buon-ma-thuot/shopping/overview",
            "https://vinpearl.com/en/buon-ma-thuot-vietnam-a-comprehensive-travel-guide"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "logistics": [
        {
          "name": "Da Nang - Buon Ma Thuot flight (VN1911)",
          "area": "Route into the highlands leg",
          "what": "The only practical way into this leg of the route: a roughly 65-minute Vietnam Airlines flight from Da Nang, operated on selected days of the week rather than daily.",
          "why": "The whole route depends on this flight existing on the chosen date; it must be checked against the calendar before booking, not assumed",
          "lat": 12.6668723,
          "lng": 108.1199878,
          "approx": false,
          "sources": [
            "https://www.vietnamairlines.com/en-vn/flights-from-da-nang-to-buon-ma-thuot",
            "https://www.flightaware.com/live/flight/HVN1911"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ]
    }
  },
  "lak-lake": {
    "id": "lak-lake",
    "name": "Lak Lake",
    "region": "highlands",
    "seq": 10,
    "lat": 12.4076,
    "lng": 108.1836,
    "color": "#808000",
    "counts": {
      "hotels": 2,
      "must_see": 1,
      "attractions": 0,
      "food": 0,
      "markets": 0,
      "logistics": 0
    },
    "poi": {
      "hotels": [
        {
          "name": "Lak Tented Camp",
          "area": "Yang Tao, Lien Son, reached only by boat",
          "what": "A small eco-lodge accessible only by boat crossing, with 15 safari-style tents, four lakeside bungalows and a wooden longhouse restaurant on the shore of Lak Lake.",
          "why": "The consensus pick of two independently-researched agent proposals for this leg, and the only proper lodge actually on the lake",
          "lat": 12.4279787,
          "lng": 108.1812233,
          "approx": true,
          "sources": [
            "https://www.booking.com/hotel/vn/lak-tented-camp.html",
            "https://www.tripadvisor.com/Hotel_Review-g3389563-d11875783-Reviews-Lak_Tented_Camp-Lien_Son_Dak_Lak_Province.html"
          ],
          "tier": 3,
          "tierOfficial": false,
          "priceLow": 60,
          "priceHigh": 160,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Bao Dai Villa (Lak Lake)",
          "area": "Hill above Lak Lake, Lien Son town",
          "what": "The 1951 hunting lodge Emperor Bao Dai built on a hill overlooking Lak Lake, now run as a simple guesthouse with the old dining room serving as a restaurant.",
          "why": "The only accommodation directly on the hill above the lake, inside a genuine former royal building",
          "lat": 12.4155999,
          "lng": 108.1816523,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g670918-d3291911-Reviews-Bao_Dai_Villa-Buon_Ma_Thuot_Dak_Lak_Province.html",
            "https://vnexpress.net/biet-dien-bao-dai-ben-ho-lak-4393734.html"
          ],
          "tier": 3,
          "tierOfficial": false,
          "priceLow": 20,
          "priceHigh": 30,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "must_see": [
        {
          "name": "Lak Lake",
          "area": "Lien Son, Lak district",
          "what": "The largest natural freshwater lake in the Central Highlands, ringed by rice paddies and forest, crossed by hand-carved dugout canoes rather than motorboats.",
          "why": "The centrepiece of this leg of the route, and the reason the itinerary stops here overnight",
          "lat": 12.4232112,
          "lng": 108.1776243,
          "approx": false,
          "sources": [
            "https://en.wikipedia.org/wiki/Lak_Lake",
            "https://www.bestpricetravel.com/travel-guide/lak-lake.html"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [],
      "food": [],
      "markets": [],
      "logistics": []
    }
  },
  "da-lat": {
    "id": "da-lat",
    "name": "Da Lat",
    "region": "highlands",
    "seq": 11,
    "lat": 11.9404,
    "lng": 108.4583,
    "color": "#469990",
    "counts": {
      "hotels": 3,
      "must_see": 3,
      "attractions": 2,
      "food": 1,
      "markets": 2,
      "logistics": 0
    },
    "poi": {
      "hotels": [
        {
          "name": "MerPerle Dalat Hotel",
          "area": "Next to Da Lat golf course",
          "what": "A large new hotel with an indoor pool, spa and its own attached winery, on the edge of downtown next to Da Lat's golf course.",
          "why": "The highest-scoring self-declared 5-star in Da Lat, though several guests say it falls short of a true 5-star standard",
          "lat": 11.9410283,
          "lng": 108.4583231,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g293922-d26305215-Reviews-MerPerle_Dalat_Hotel-Da_Lat_Lam_Dong_Province.html",
            "https://www.kayak.com/Dalat-Hotels-Merperle-Dalat-Hotel.9967439.ksp"
          ],
          "tier": 5,
          "tierOfficial": false,
          "priceLow": 55,
          "priceHigh": 91,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Colline Dalat",
          "area": "Next to Da Lat night market",
          "what": "A 150-room modern hotel built directly onto the steps down to Da Lat's night market, with a rooftop restaurant looking over the town.",
          "why": "Officially 4-star and zero steps from the night market; the master-spec's top pick for Da Lat",
          "lat": 11.94397,
          "lng": 108.438126,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g293922-d16731336-Reviews-Colline-Da_Lat_Lam_Dong_Province.html",
            "https://us.trip.com/hotels/dalat-hotel-detail-29515862/colline-dalat/"
          ],
          "tier": 4,
          "tierOfficial": true,
          "priceLow": 63,
          "priceHigh": 76,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Terracotta Hotel & Resort Dalat",
          "area": "Lakeside, near Da Lat golf course",
          "what": "A spa hotel on the shore of a small private lake, with two restaurants, bike rental and an adjoining golf course.",
          "why": "A genuine lakeside 4-star property at close to 3-star prices",
          "lat": 11.894725,
          "lng": 108.4397193,
          "approx": true,
          "sources": [
            "https://www.momondo.com/hotels/da-lat/Terracotta-Hotel-Resort-Dalat.mhd2272019.ksp",
            "https://www.makemytrip.com/hotels-international/en-us/vietnam/dalat-hotels/terracotta_hotel_resort_dalat-details.html"
          ],
          "tier": 4,
          "tierOfficial": false,
          "priceLow": 44,
          "priceHigh": 53,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "must_see": [
        {
          "name": "Crazy House (Hang Nga Guesthouse)",
          "area": "Huynh Thuc Khang Street",
          "what": "A surreal building shaped like a giant banyan tree, designed by architect Dang Viet Nga with tunnel staircases, mushroom-shaped rooms and almost no straight lines anywhere.",
          "why": "Unlike anything else built in Vietnam, and walkable from the city centre",
          "lat": 11.9345622,
          "lng": 108.4305116,
          "approx": true,
          "sources": [
            "https://www.cnn.com/travel/article/crazy-house-dalat-vietnam",
            "https://vinwonders.com/en/wonderpedia/news/dalat-crazy-house/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Langbiang Mountain",
          "area": "Lac Duong, ~12km north of the city",
          "what": "A 2,167m twin-peaked mountain reached by a bumpy 4.5km jeep track from its base, with panoramic views over Da Lat's pine forests and valleys from the summit.",
          "why": "The best viewpoint over the whole Da Lat plateau, and an easy half-day trip",
          "lat": 12.0472573,
          "lng": 108.4405826,
          "approx": false,
          "sources": [
            "https://vinwonders.com/en/wonderpedia/news/lang-biang-mountain-dalat/",
            "https://localvietnam.com/blog/langbiang-mountain/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Xuan Huong Lake",
          "area": "City center",
          "what": "A 40-hectare artificial lake built by French colonists in 1919 at the centre of Da Lat, ringed by a walking path, pine trees and the old golf course.",
          "why": "Da Lat organises itself around this lake the way Hanoi organises itself around Hoan Kiem",
          "lat": 11.9450803,
          "lng": 108.4487222,
          "approx": false,
          "sources": [
            "https://vinwonders.com/en/wonderpedia/news/xuan-huong-lake-dalat/",
            "https://www.tripadvisor.com/Attraction_Review-g293922-d451022-Reviews-Xuan_Huong_Lake-Da_Lat_Lam_Dong_Province.html"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [
        {
          "name": "Datanla Waterfall Canyoning",
          "area": "7km south of the city",
          "what": "A guided descent through the Datanla waterfall gorge from a base camp at the falls: rappelling down cliffs and a 30m waterfall, a zipline, a water slide and a narrow rock chute nicknamed the 'washing machine'.",
          "why": "Da Lat's real adventure-sport claim, and one of the few canyoning operations anywhere in Vietnam",
          "lat": 11.9011774,
          "lng": 108.4488444,
          "approx": false,
          "sources": [
            "https://tinggly.com/experience/canyoning-2400m-alpine-coaster-activity-in-dalat/141620P6",
            "https://www.tripadvisor.com/AttractionProductReview-g293922-d27116487-Canyoning_2400m_Alpine_Coaster_Activity_in_Dalat-Da_Lat_Lam_Dong_Province.html"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Tuyen Lam Lake SUP/Kayak and Clay Tunnel",
          "area": "Tuyen Lam Lake, south of the city",
          "what": "A paddle by kayak or stand-up paddleboard across Tuyen Lam Lake's pine-fringed water, usually combined with a stop at the Clay Tunnel, a walk-through open-air clay sculpture near the Truc Lam monastery.",
          "why": "The quiet, uncrowded counterpart to the night market; nature and folk art in one outing",
          "lat": 11.8907954,
          "lng": 108.4250836,
          "approx": false,
          "sources": [
            "https://powertraveller.com/da-lat-tuyen-lam-lake-kayak-or-sup-tour/",
            "https://kayawanderlust.com/self-guided-tour-to-the-clay-tunnel-and-truc-lam-monastery/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "food": [
        {
          "name": "Artichoke tea (Tra Atiso) at Da Lat Market",
          "area": "Da Lat Market, city center",
          "what": "Dried artichoke flower heads, grown on the plateau around Da Lat, sold loose or bagged as a bitter herbal tea at stalls throughout Da Lat Market.",
          "why": "Da Lat grows most of Vietnam's artichoke crop; the tea is the plateau's signature souvenir",
          "lat": 11.9435196,
          "lng": 108.4372097,
          "approx": false,
          "sources": [
            "https://tamtrinhcoffee.com/da-lat-specialty-gifts/",
            "https://www.expatolife.com/things-to-buy-shopping-da-lat-vietnam/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "local_media",
          "video": null
        }
      ],
      "markets": [
        {
          "name": "Da Lat Market (Cho Da Lat)",
          "area": "City center, beside Xuan Huong Lake",
          "what": "The city's main covered market building on a hillside above Xuan Huong Lake, selling fresh produce, dried flowers, hot street food and Da Lat's own coffee and wine.",
          "why": "The daytime anchor of Da Lat's market district, a few steps from the lake",
          "lat": 11.9435196,
          "lng": 108.4372097,
          "approx": false,
          "sources": [
            "https://en.wikipedia.org/wiki/Da_Lat_Market",
            "https://vinwonders.com/en/wonderpedia/news/dalat-market/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Da Lat Night Market (Cho Am Phu)",
          "area": "Steps below Da Lat Market, city center",
          "what": "The streets and steps below the market building come alive after 5pm with food stalls, grilled rice paper, hot soy milk and fresh strawberries, plus clothing and souvenir stalls.",
          "why": "Da Lat's evening centre of gravity, and where most of the specialty street food listed here is actually eaten",
          "lat": 11.9414964,
          "lng": 108.4372724,
          "approx": true,
          "sources": [
            "https://vinpearl.com/en/da-lat-night-market",
            "https://www.vietnamtourism.org.vn/travel-guide/destination-in-vietnam/da-lat%E2%80%99s-night-market.html"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "logistics": []
    }
  },
  "saigon": {
    "id": "saigon",
    "name": "Ho Chi Minh City",
    "region": "south",
    "seq": 12,
    "lat": 10.7769,
    "lng": 106.7009,
    "color": "#000075",
    "counts": {
      "hotels": 3,
      "must_see": 1,
      "attractions": 2,
      "food": 2,
      "markets": 1,
      "logistics": 2
    },
    "poi": {
      "hotels": [
        {
          "name": "Hotel Des Arts Saigon - MGallery",
          "area": "District 1, near Notre-Dame Cathedral",
          "what": "A 5-star Art Deco-era building restored as an Accor MGallery hotel, with 168 rooms, a rooftop infinity pool and a French colonial facade a short walk from Notre-Dame Cathedral.",
          "why": "Accor-chain 5-star with an officially assigned rating, mentioned as an alternative in the project's own vetted hotel research",
          "lat": 10.7820238,
          "lng": 106.6971407,
          "approx": true,
          "sources": [
            "https://www.hoteldesartssaigon.com/",
            "https://www.tripadvisor.com/Hotel_Review-g293925-d8142973-Reviews-Hotel_Des_Arts_Saigon_Mgallery-Ho_Chi_Minh_City.html"
          ],
          "tier": 5,
          "tierOfficial": true,
          "priceLow": 134,
          "priceHigh": 396,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Silverland Central Hotel",
          "area": "District 1, near Ben Thanh Market",
          "what": "A 101-room officially-rated 3-star boutique hotel a short walk from Ben Thanh Market, part of the long-running Silverland hotel group, with a rooftop bar called OMG.",
          "why": "Officially classified 3-star (not self-declared) with a decade of top-ten 3-star rankings in the city",
          "lat": 10.7718774,
          "lng": 106.6972524,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g293925-d1178145-Reviews-Silverland_Central_Hotel-Ho_Chi_Minh_City.html",
            "https://silverlandhotels.com/"
          ],
          "tier": 3,
          "tierOfficial": true,
          "priceLow": 177,
          "priceHigh": 188,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Bong Sen Hotel Saigon",
          "area": "District 1, Dong Khoi Street",
          "what": "A 120-room 3-star hotel on Dong Khoi, the city's main shopping street, with three restaurants and a small fitness center.",
          "why": "Officially rated 3-star on the same street as the 5-star picks, at a fraction of the price",
          "lat": 10.7751171,
          "lng": 106.7038852,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g293925-d1748426-Reviews-Bong_Sen_Hotel_Saigon-Ho_Chi_Minh_City.html",
            "https://www.booking.com/hotel/vn/bong-sen-saigon.html"
          ],
          "tier": 3,
          "tierOfficial": true,
          "priceLow": 48,
          "priceHigh": 94,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "must_see": [
        {
          "name": "Reunification Palace",
          "area": "District 1",
          "what": "A 1960s modernist government building where a North Vietnamese tank crashed through the gates on 30 April 1975. The war rooms, radio room and presidential quarters are preserved as they were that day.",
          "why": "The single physical location where the Vietnam War's ending is preserved in place, not just described",
          "lat": 10.7770348,
          "lng": 106.695488,
          "approx": false,
          "sources": [
            "https://www.getyourguide.com/explorer/ho-chi-minh-ttd272/landmarks-in-ho-chi-minh-city/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [
        {
          "name": "Cu Chi Tunnels",
          "area": "Cu Chi District, about 1.5 hours from central Saigon",
          "what": "A preserved section of the more than 120 km of hand-dug underground tunnel network used by Viet Cong fighters, with widened crawl-through sections, hidden trapdoor entrances and reconstructed underground rooms.",
          "why": "The signature half-day trip from Saigon, and one of the few places in Vietnam you physically enter the war rather than just read about it",
          "lat": 11.0630436,
          "lng": 106.5291244,
          "approx": false,
          "sources": [
            "https://www.holidify.com/places/ho-chi-minh-city/sightseeing-and-things-to-do.html"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "War Remnants Museum",
          "area": "District 3",
          "what": "A three-storey museum housing over 20,000 artifacts, photographs and military hardware across nine permanent exhibitions on the Vietnam War and its aftermath, including an outdoor yard of captured US tanks and aircraft.",
          "why": "The most direct, unfiltered account of the war from the Vietnamese side, consistently rated the city's top museum",
          "lat": 10.7793647,
          "lng": 106.6922806,
          "approx": false,
          "sources": [
            "https://ahoyvietnam.com/war-remnants-museum/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "food": [
        {
          "name": "Anan Saigon",
          "area": "District 1, Cho Cu (Old Market)",
          "what": "A restaurant built inside a former wet-market stall on Ton That Dam Street, where chef Peter Cuong Franklin runs street-food recipes through French fine-dining technique.",
          "why": "One Michelin Star, held since 2023, and the clearest example of Saigon's fine-dining scene built on its own street food",
          "lat": 10.7718032,
          "lng": 106.7029748,
          "approx": false,
          "sources": [
            "https://guide.michelin.com/en/ho-chi-minh/ho-chi-minh_2978179/restaurant/anan-saigon",
            "https://anansaigon.com/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "michelin_star",
          "video": null
        },
        {
          "name": "Banh Mi Huynh Hoa",
          "area": "District 1",
          "what": "A takeaway counter open since 1989 with a permanent line out front, packing a baguette with five cold cuts, pate, butter and pickles.",
          "why": "Widely cited as the single most-loaded, most-recommended banh mi in the city, voted Travelers' Top Pick at the 2024 Flavors Awards",
          "lat": 10.7713922,
          "lng": 106.6927189,
          "approx": true,
          "sources": [
            "https://vietcetera.com/en/banh-mi-huynh-hoa-how-100k-and-35-years-built-a-saigon-icon",
            "https://www.tripadvisor.com/Restaurant_Review-g293925-d5484355-Reviews-Banh_Mi_Huynh_Hoa-Ho_Chi_Minh_City.html"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "traveler_recommended",
          "video": null
        }
      ],
      "markets": [
        {
          "name": "Ben Thanh Market",
          "area": "District 1",
          "what": "A covered market of nearly 1,450 stalls under a French-built 1914 clock-tower facade, selling everything from produce and dried goods to clothing, souvenirs and a food court, spilling into a street-food night market outside after dark.",
          "why": "The city's oldest and largest market, and the default orientation point for District 1",
          "lat": 10.7725301,
          "lng": 106.6980365,
          "approx": false,
          "sources": [
            "https://oxalisadventure.com/ben-thanh-market-ho-chi-minh-city/",
            "https://vinwonders.com/en/wonderpedia/news/ben-thanh-market-a-prominent-landmark-of-the-bustling-ho-chi-minh-city/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "logistics": [
        {
          "name": "Grab from Tan Son Nhat Airport",
          "area": "Tan Son Nhat International Airport (SGN)",
          "what": "Ride-hailing pickup for Grab cars is outside the arrivals hall, past the metered-taxi rank; a ride to District 1 takes 25-50 minutes depending on traffic and costs roughly 110,000-250,000 VND.",
          "why": "Cheaper and more predictable than the taxi rank, with a fixed upfront fare shown before booking",
          "lat": 10.8179793,
          "lng": 106.6562645,
          "approx": false,
          "sources": [
            "https://blog.gettransfer.com/from-ho-chi-minh-city-airport-to-the-city-center-taxi-grab-more/",
            "https://www.grab.com/global/airport-rides/tan-son-nhat-international-airport/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "No airport metro link yet",
          "area": "Tan Son Nhat International Airport (SGN)",
          "what": "Saigon's first metro line (Line 1, Ben Thanh-Suoi Tien) opened in December 2024, but no metro or rail line reaches the airport; a dedicated airport link is not expected until around 2030.",
          "why": "Rules out the metro as an airport option, which travelers researching the new 2024 line sometimes assume is already connected",
          "lat": 10.8179793,
          "lng": 106.6562645,
          "approx": false,
          "sources": [
            "https://aifly.one/2026/03/ho-chi-minh-city-tan-son-nhat-airport-guide/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ]
    }
  },
  "mekong": {
    "id": "mekong",
    "name": "Mekong and Can Tho",
    "region": "south",
    "seq": 13,
    "lat": 10.0452,
    "lng": 105.7469,
    "color": "#800000",
    "counts": {
      "hotels": 4,
      "must_see": 1,
      "attractions": 2,
      "food": 2,
      "markets": 0,
      "logistics": 1
    },
    "poi": {
      "hotels": [
        {
          "name": "Sheraton Can Tho",
          "area": "Ninh Kieu, riverside",
          "what": "The tallest international hotel in the Mekong Delta, on the Can Tho riverfront near Ninh Kieu Pier and the night market, formerly branded as Vinpearl Hotel Can Tho before its rebrand under Marriott.",
          "why": "The only internationally-chained 5-star in the Mekong Delta, confirmed by multiple independent sources as officially rated",
          "lat": 10.0242294,
          "lng": 105.7744816,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g303942-d11743875-Reviews-Sheraton_Can_Tho-Can_Tho_Mekong_Delta.html",
            "https://www.marriott.com/en-us/hotels/vcasi-sheraton-can-tho/overview/"
          ],
          "tier": 5,
          "tierOfficial": true,
          "priceLow": 61,
          "priceHigh": 200,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Victoria Can Tho Resort",
          "area": "Riverside, Cai Khe islet",
          "what": "A colonial-style riverside resort from the established Victoria hotels chain, with a pool overlooking the Can Tho River and its own daily Mekong boat tours for guests.",
          "why": "The delta's best-regarded conventional resort chain, officially rated and consistently praised over the larger conference hotels in town",
          "lat": 10.0393054,
          "lng": 105.7930514,
          "approx": false,
          "sources": [
            "https://www.travelfish.org/accommodation_profile/vietnam/mekong_delta/can_tho/can_tho/all/8497",
            "https://www.tripadvisor.com/Hotel_Review-g303942-d306941-Reviews-Victoria_Can_Tho_Resort-Can_Tho_Mekong_Delta.html"
          ],
          "tier": 4,
          "tierOfficial": true,
          "priceLow": 71,
          "priceHigh": 95,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Can Tho Ecolodge",
          "area": "Cai Rang, Ba Lang River",
          "what": "A thatched-house eco-resort on the Ba Lang River outside town, with a pool, garden and bar, built around responsibly showcasing the surrounding delta rather than a conventional hotel tower.",
          "why": "The most resort-like eco-lodge option in the area, ranked third of Can Tho's specialty lodging with consistently strong reviews",
          "lat": 9.9878302,
          "lng": 105.7414525,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g303942-d17528812-Reviews-Can_Tho_Ecolodge-Can_Tho_Mekong_Delta.html",
            "https://www.booking.com/hotel/vn/can-tho-ecolodge.en-gb.html"
          ],
          "tier": 4,
          "tierOfficial": false,
          "priceLow": 56,
          "priceHigh": 82,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Bamboo Eco Village",
          "area": "Can Tho outskirts",
          "what": "A small officially 3-star eco-hotel with a garden, pool and bicycles for guests, built around orchard and canal surroundings rather than a town-centre location.",
          "why": "Officially rated 3-star with unusually strong reviews for the tier, praised repeatedly for the garden and pool",
          "lat": 10.0074606,
          "lng": 105.7054798,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g303942-d19602577-Reviews-Bamboo_Eco_Village-Can_Tho_Mekong_Delta.html",
            "https://en.planetofhotels.com/vietnam/can-tho/bamboo-eco-village"
          ],
          "tier": 3,
          "tierOfficial": true,
          "priceLow": 33,
          "priceHigh": 56,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "must_see": [
        {
          "name": "Cai Rang Floating Market",
          "area": "Cai Rang, about 6 km southwest of central Can Tho",
          "what": "A river market of roughly 200-300 local trading boats and produce barges, each hanging a sample of its goods from a tall pole so buyers can spot it from the water. It runs from before sunrise and is essentially over as a wholesale market by mid-morning.",
          "why": "The largest and most authentic floating market left in the delta, but only if timed for its real dawn trading hours, not a mid-morning visit",
          "lat": 10.0023957,
          "lng": 105.7443925,
          "approx": false,
          "sources": [
            "https://vemekong.com/guide-to-can-tho-floating-markets/",
            "https://www.travelfish.org/sight_profile/vietnam/mekong_delta/can_tho/can_tho/2496"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [
        {
          "name": "My Tho and Ben Tre coconut candy village",
          "area": "My Tho and Ben Tre provinces, upper Mekong Delta",
          "what": "A river-island circuit reached by motorboat and narrow-canal sampan (a small wooden boat rowed by a boatman in a conical hat), stopping at a small workshop where coconut milk is hand-cooked and cut into candy while still warm.",
          "why": "The classic, gentler alternative to Can Tho for a single-day Mekong visit, and the standard way to see hand-made coconut candy production",
          "lat": 10.0163692,
          "lng": 105.7379094,
          "approx": true,
          "sources": [
            "https://viet-go.com/en/attractions/my-tho-ben-tre-mekong-delta-guide"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Vinh Trang Pagoda",
          "area": "My Tho",
          "what": "A 19th-century Buddhist pagoda recognised as a national historical relic, blending Vietnamese, Khmer and French architectural styles with a large reclining Buddha statue in its grounds.",
          "why": "The most architecturally distinct temple in the delta, mixing three building traditions in one compound",
          "lat": 10.3628375,
          "lng": 106.3735689,
          "approx": false,
          "sources": [
            "https://www.viator.com/Mekong-Delta-attractions/Vinh-Trang-Pagoda/d23962-a19069"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "food": [
        {
          "name": "Lua Nep",
          "area": "Ninh Kieu riverside, Can Tho",
          "what": "A riverside restaurant serving the delta's signature elephant ear fish, fried whole and served upright so the flesh is rolled into rice paper with herbs and pickles at the table.",
          "why": "Repeatedly singled out by recent travelers for this specific dish, the Mekong Delta's most iconic",
          "lat": 10.0450175,
          "lng": 105.7947956,
          "approx": false,
          "sources": [
            "https://hanoivoyage.com/en/blog/restaurant/top-7-restaurants-in-the-mekong-delta"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "traveler_recommended",
          "video": null
        },
        {
          "name": "Sao Hom Restaurant",
          "area": "Ninh Kieu riverside, Can Tho, inside the old Nha Long market building",
          "what": "A restaurant set inside a restored early-1900s riverside market hall, with open river views and a menu of southern Vietnamese home cooking.",
          "why": "A local guide recommendation for a proper sit-down dinner, in one of Can Tho's most distinctive dining buildings",
          "lat": 10.0313789,
          "lng": 105.7882653,
          "approx": false,
          "sources": [
            "https://vinwonders.com/en/wonderpedia/news/can-tho-restaurants/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": "vietnamese",
          "signal": "traveler_recommended",
          "video": null
        }
      ],
      "markets": [],
      "logistics": [
        {
          "name": "Bus from Ho Chi Minh City to Can Tho",
          "area": "Ho Chi Minh City to Can Tho, roughly 170 km",
          "what": "A sleeper coach (commonly the Futa/Phuong Trang line) covers the route in about 3 hours of driving, though the door-to-door trip including rest stops and pickup/drop-off typically runs closer to 5 hours; a taxi from the Can Tho bus station to Ninh Kieu Wharf adds about 15 minutes.",
          "why": "The standard overland option between the two, and the reason a Mekong stop is usually built around an overnight rather than a rushed day trip",
          "lat": 10.0243445,
          "lng": 105.7615442,
          "approx": false,
          "sources": [
            "https://vemekong.com/guide-to-can-tho-floating-markets/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ]
    }
  },
  "phu-quoc": {
    "id": "phu-quoc",
    "name": "Phu Quoc",
    "region": "south",
    "seq": 14,
    "lat": 10.2899,
    "lng": 103.984,
    "color": "#a9a9a9",
    "counts": {
      "hotels": 3,
      "must_see": 1,
      "attractions": 1,
      "food": 0,
      "markets": 1,
      "logistics": 2
    },
    "poi": {
      "hotels": [
        {
          "name": "Sheraton Phu Quoc Long Beach Resort",
          "area": "Long Beach, Ganh Dau",
          "what": "A large Marriott-chain beachfront resort on Long Beach with multiple pools, several restaurants and direct sand access.",
          "why": "Officially rated 5-star with an international chain standard, and its entry-level rooms stay under the trip's price cap despite the brand",
          "lat": 10.3375473,
          "lng": 103.8498843,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g12666019-d8774806-Reviews-Sheraton_Phu_Quoc_Long_Beach_Resort-Ganh_Dau_Phu_Quoc_Island_Kien_Giang_Province.html",
            "https://www.momondo.com/hotels/phu-quoc/Sheraton-Phu-Quoc-Long-Beach-Resort.mhd2449378.ksp"
          ],
          "tier": 5,
          "tierOfficial": true,
          "priceLow": 97,
          "priceHigh": 200,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "L'Azure Resort and Spa",
          "area": "Duong Dong",
          "what": "A small rustic-eco resort with a private sand beach, pool and spa, officially rated 4-star, built around a low-rise, garden-heavy design rather than a tower.",
          "why": "Officially rated 4-star with a 9.4-9.5 guest score, and the most consistently well-reviewed 4-star in the pool",
          "lat": 10.2080717,
          "lng": 103.9616615,
          "approx": false,
          "sources": [
            "https://www.tripadvisor.com/Hotel_Review-g1184679-d640629-Reviews-L_Azure_Resort_and_Spa-Duong_Dong_Phu_Quoc_Island_Kien_Giang_Province.html",
            "https://www.makemytrip.com/hotels-international/vietnam/phu_quoc-hotels/l_azure_resort_and_spa-details.html"
          ],
          "tier": 4,
          "tierOfficial": true,
          "priceLow": 63,
          "priceHigh": 115,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "AVS Hotel Phu Quoc",
          "area": "Duong Dong, 100m from the beach",
          "what": "A modern mid-size hotel a hundred metres from the beach, officially rated 4-star, with a pool, spa and airport transfers.",
          "why": "Officially rated 4-star, ranked in the top 20 hotels on the island by guest reviews despite its budget-adjacent price",
          "lat": 10.2007569,
          "lng": 103.9638791,
          "approx": false,
          "sources": [
            "https://en.planetofhotels.com/vietnam/phu-quoc/avs-hotel-phu-quoc",
            "https://www.tripadvisor.com/Hotel_Review-g1184679-d20200026-Reviews-AVS_Hotel_Phu_Quoc-Duong_Dong_Phu_Quoc_Island_Kien_Giang_Province.html"
          ],
          "tier": 4,
          "tierOfficial": true,
          "priceLow": 46,
          "priceHigh": 156,
          "priceChecked": "2026-08-16",
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "must_see": [
        {
          "name": "Hon Thom Cable Car",
          "area": "An Thoi, southern Phu Quoc",
          "what": "A three-cable gondola line running almost 8 km from the An Thoi coast over open sea to Hon Thom island, in 30-passenger cabins over a 15-minute ride, passing above two smaller islands en route.",
          "why": "Guinness World Record holder for the longest three-wire sea-crossing cable car, and the way most visitors reach Hon Thom's Sun World park",
          "lat": 9.9920077,
          "lng": 104.0124425,
          "approx": false,
          "sources": [
            "https://blog.premierresidencesphuquoc.com/hon-thom-cable-car/",
            "https://www.vietjetair.com/en/news/travel-guides-1665635013747/hon-thom-phu-quoc-cable-car-review-the-worlds-longest-sea-crossing-cable-car-1768878737803"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "attractions": [
        {
          "name": "Vinpearl Safari Phu Quoc",
          "area": "Bai Dai, northwest Phu Quoc",
          "what": "Vietnam's largest wildlife conservation park, home to roughly 4,500 animals across 200 species including Bengal tigers, African lions, giraffes and white rhinos, viewable from a safari-style drive-through zone and walking areas.",
          "why": "The largest wildlife park in the country, and a full-day option that doesn't require a beach or a boat",
          "lat": 10.3393964,
          "lng": 103.8950113,
          "approx": true,
          "sources": [
            "https://vinwonders.com/en/wonderpedia/news/review-of-vinpearl-safari-phu-quoc/",
            "https://www.tripadvisor.com/Attraction_Review-g469418-d9748314-Reviews-Vinpearl_Safari_Phu_Quoc-Phu_Quoc_Island_Kien_Giang_Province.html"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "food": [],
      "markets": [
        {
          "name": "Phu Quoc Night Market (Dinh Cau)",
          "area": "Duong Dong, Bach Dang street",
          "what": "A single-street night market where diners pick live fish, crab or squid from tanks to be grilled or steamed to order, alongside stalls selling herring salad, banh xeo pancakes and grilled scallops.",
          "why": "The island's main after-dark food destination since its 2016 merger with the old Dinh Cau market, and the best single stop for trying local seafood specialties in one place",
          "lat": 10.3242259,
          "lng": 103.8581673,
          "approx": true,
          "sources": [
            "https://www.baconismagic.ca/vietnam/phu-quoc-night-market/",
            "https://vinwonders.com/en/wonderpedia/news/phu-quoc-night-market/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ],
      "logistics": [
        {
          "name": "Grab and taxi from Phu Quoc International Airport",
          "area": "Phu Quoc International Airport (PQC), about 10 km south of Duong Dong",
          "what": "Grab and metered taxis both operate from the terminal; a ride to the Long Beach hotel strip takes about 10-15 minutes and costs roughly 100,000-200,000 VND, with Grab typically 10-20% cheaper than the metered taxi rate.",
          "why": "The airport sits close enough to the main hotel strip that a transfer is short and cheap regardless of which resort is booked",
          "lat": 10.1727084,
          "lng": 103.9921557,
          "approx": false,
          "sources": [
            "https://www.airporttransferportal.com/airport-guides/pqc/cost-to-city",
            "https://www.grab.com/global/airport-rides/phu-quoc-international-airport/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        },
        {
          "name": "Speedboat from the Mekong Delta (Ha Tien)",
          "area": "Ha Tien to Bai Vong pier, Phu Quoc",
          "what": "Fast boats from Ha Tien on the Mekong Delta coast to Phu Quoc's Bai Vong pier run 3-5 times daily between about 6am and 2pm, taking roughly 1.5 hours; slower car ferries take about 3 hours on the same route.",
          "why": "Connects a Mekong Delta stop directly to Phu Quoc without backtracking through Ho Chi Minh City for a flight",
          "lat": 10.1457488,
          "lng": 104.038743,
          "approx": false,
          "sources": [
            "https://www.vietnamcoracle.com/phu-quoc-island-ferry-times/"
          ],
          "tier": null,
          "priceLow": null,
          "priceHigh": null,
          "avoid": false,
          "kind": null,
          "signal": null,
          "video": null
        }
      ]
    }
  }
};
