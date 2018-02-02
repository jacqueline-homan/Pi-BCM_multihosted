{% load static %}

$('[name=package_type]').on('change', function (e) {
    var packagingTypeData = {
        1:
            {
                src: "{% static 'products/site/wizard/proddesc/BG.png' %}",
                desc: "A preformed, flexible container, generally enclosed on all but one side, which forms an opening that may or may not be sealed after filling."
            },

        2:
            {
                src: "{% static 'products/site/wizard/proddesc/BPG.png' %}",
                desc: "A type of packaging in which the item is secured between a preformed (usually transparent plastic) dome or “bubble” and a paperboard surface or “carrier.”  Attachment may be by stapling, heat-sealing, gluing, or other means.  In other instances, the blister folds over the product in clam-shell fashion to form an enclosing container.  Blisters are most usually thermoformed from polyvinyl chloride; however, almost any thermoplastic can be thermoformed into a blister."
            },

        3:
            {
                src: "{% static 'products/site/wizard/proddesc/BO.png' %}",
                desc: "A container having a round neck of relatively smaller diameter than the body and an opening capable of holding a closure for retention of the contents. Specifically, a narrow-necked container as compared with a jar or wide-mouth container. The cross section of the bottle may be round, oval, square, oblong, or a combination of these. Bottles generally are made of glass or plastics, but can also be earthenware or metal. Bottle may be disposable, recyclable, returnable, or reusable."
            },

        4:
            {
                src: "{% static 'products/site/wizard/proddesc/BX.png' %}",
                desc: "A non-specific term used to refer to a rigid, three- dimensional container with closed faces that completely enclose its contents and may be made out of any material. Even though some boxes might be reused or become resealed they could also be disposable depending on the product hierarchy."
            },

        5:
            {
                src: "{% static 'products/site/wizard/proddesc/CNG.png' %}",
                desc: "A metallic and generally cylindrical container of unspecified size which can be used for items of consumer and institutional sizes."
            },

        6:
            {
                src: "{% static 'products/site/wizard/proddesc/CM.png' %}",
                desc: "A flat package to which the product is hung or attached for display."
            },

        8:
            {
                src: "{% static 'products/site/wizard/proddesc/JG.png' %}",
                desc: "A container, normally cylindrical, with a handle and/or a lid or spout for holding and pouring liquids"
            },

        9:
            {
                src: "{% static 'products/site/wizard/proddesc/ZU.png' %}",
                desc: "A non-rigid container used for transport and storage of fluids and other bulk materials. The construction of the IBC container and the materials used are chosen depending on the application."
            },

        10:
            {
                src: "{% static 'products/site/wizard/proddesc/MPG.png' %}",
                desc: "A bundle of products held together for ease of carriage by the consumer. A multipack is always a consumer unit."
            },

        14:
            {
                src: "{% static 'products/site/wizard/proddesc/PU.png' %}",
                desc: "A shallow container, which may or may not have a cover, used for displaying, carrying items or carry for warehousing.  Examples for TIIG • Plate  • Cardboard carrier  • Cellplate  • Divider Sheet/Slip Sheet  • Plastic-Wrapped Tray  • Tray for bottles  • Tray one layer no cover  • Tray tablet  • Tray Shrinkpacked  • Tray/Tray pack  • Other Information  • This code also covers all &#39;ready to cook&#39; plates in which some products are sold.  • Divider Sheets/Slip Sheets which are used to hold layers on a pallet for efficient cross docking warehousing processes. "
            },

        15:
            {
                src: "{% static 'products/site/wizard/proddesc/CU.png' %}",
                desc: "A flat-bottomed container that has a base of any shape and which may or not be closed with a lid. Usually made of paper, plastic or other materials these containers are typically used to contain mostly (but not exclusively) foods such as ice cream, margarine, yogurt, sour cream, confections, etc. "
            },

        16:
            {
                src: "{% static 'products/site/wizard/proddesc/TU.png' %}",
                desc: "A cylindrical container sealed on one end that could be closed with a cap or dispenser on the other end."
            },

        17:
            {
                src: "{% static 'products/site/wizard/proddesc/NE.png' %}",
                desc: "The item is provided without packaging"
            },

        19:
            {
                src: "{% static 'products/site/wizard/proddesc/AE.png' %}",
                desc: "A gas-tight, pressure-resistant container with a valve and propellant. When the valve is opened, propellant forces the product from the container in a fine or coarse spray pattern or stream. (e.g., a spray can dispensing paint, furniture polish, etc, under pressure). It does not include atomizers, because atomizers do not rely on a pressurised container to propel product from the container."
            },

        21:
            {
                src: "{% static 'products/site/wizard/proddesc/CT.png' %}",
                desc: "A non-specific term for an open or re-closable container used mostly for perishable foods (e.g. eggs, or fruit)."
            },

        22:
            {
                src: "{% static 'products/site/wizard/proddesc/PUG.png' %}",
                desc: "Packaging of the product (or products) is currently not on the list. Use this code when no suitable options are available and only while a Change Request is approved for the proper packaging type."
            },

        25:
            {
                src: "{% static 'products/site/wizard/proddesc/AA.png' %}",
                desc: "A Rigid Intermediate Bulk Container (RIBC) that is attached to a pallet or has the pallet integrated into the RIBC. The container is used for the transport and storage of fluids and other bulk materials."
            },

        30:
            {
                src: "{% static 'products/site/wizard/proddesc/BRI.png' %}",
                desc: "A rectangular-shaped, stackable package designed primarily for liquids such as juice or milk"
            },

        33:
            {
                src: "{% static 'products/site/wizard/proddesc/CR.png' %}",
                desc: "A non-specific term usually referring to a rigid three- dimensional container with semi-closed faces that enclose its contents for shipment or storage. Crates could have an open or closed top and may have internal divers. Even though some crates might be reused or become resealed they could also be disposable depending on the product hierarchy."
            },

        34:
            {
                src: "{% static 'products/site/wizard/proddesc/CS.png' %}",
                desc: "A non-specific term for a container designed to hold, house, and sheath or encase its content while protecting it during distribution, storage and/or exhibition. Cases are mostly intended to store and preserve its contents during the product&#39;s entire lifetime."
            },

        35:
            {
                src: "{% static 'products/site/wizard/proddesc/CY.png' %}",
                desc: "A rigid cylindrical container with straight sides and circular ends of equal size."
            },

        37:
            {
                src: "{% static 'products/site/wizard/proddesc/GTG.png' %}",
                desc: "A rectangular-shaped, non-stackable package designed primarily for liquids such as juice or milk"
            },

        38:
            {
                src: "{% static 'products/site/wizard/proddesc/JR.png' %}",
                desc: "A rigid container made of glass, stone, earthenware, plastic or other appropriate material with a large opening, which is used to store products, (e.g., jams, cosmetics)."
            },

        42:
            {
                src: "{% static 'products/site/wizard/proddesc/PO.png' %}",
                desc: "A preformed, flexible container, generally enclosed with a gusset seal at the bottom of the pack can be shaped/arranged to allow the pack to stand on shelf."
            },

        47:
            {
                src: "{% static 'products/site/wizard/proddesc/STR.png' %}",
                desc: "In packaging, a high-tensile plastic film, stretched and wrapped repeatedly around an item or group of items to secure and maintain unit integrity.  The use of stretch film to tightly wrap a package or a unit load in order to bind, protect and immobilize it for further handling or shipping."
            },

        48:
            {
                src: "{% static 'products/site/wizard/proddesc/SW.png' %}",
                desc: "In packaging, a plastic film around an item or group of items which is heated causing the film to shrink, securing the unit integrity. The use of shrunken film to tightly wrap a package or a unit load in order to bind, protect and immobilize it for further handling or shipping."
            },

        49:
            {
                src: "{% static 'products/site/wizard/proddesc/SY.png' %}",
                desc: "A non-rigid container usually made of paper, cardboard or plastic, that is open-ended and is slid over the contents for protection or presentation."
            },

        50:
            {
                src: "{% static 'products/site/wizard/proddesc/WRP.png' %}",
                desc: "The process of enclosing all or part of an item with layers of flexible wrapping material (e.g., for an individually packed ice cream). Does not include items which are shrink-wrapped or vacuum-packed."
            },

        51:
            {
                src: "{% static 'products/site/wizard/proddesc/X11.png' %}",
                desc: "Something used to bind, tie, or encircle the item or its packaging to secure and maintain unit integrity."
            }
    };
    var package_value = $(this).val();
    var picture_path = packagingTypeData[package_value]['src'];
    var desc = packagingTypeData[$(this).val()]['desc'];
    $('#bar_placement_img').attr("src", picture_path);
    // $('#bar_placement').val(picture_path);
    $('#description').html(desc);
});