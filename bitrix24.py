from random import random


from fast_bitrix24.bitrix import Bitrix

bx24 = Bitrix('https://expertcentre.bitrix24.ru/rest/104/9vtz15qiyfngaywx/')


# FUNCTION ASSIGNS LEAD TO MANAGER
def assignLead(
        bx_24=bx24, company_inn="", get_main_all="", managers="", eruz_member_link="", eruz_registry_date="", nalog_reg_date="",
        tip_uchastnika="", boss_title="", boss_full_name="", boss_last_name="", boss_first_name="", boss_second_name="",
        company_email="", full_company_name="", short_company_name="", company_address="", company_cell="",
        company_phone="", company_site="", cased_names_one="", cased_names_two=""
):
    print(
        company_inn, get_main_all, managers, eruz_member_link, eruz_registry_date, nalog_reg_date, tip_uchastnika,
        boss_title, boss_full_name, boss_last_name, boss_first_name, boss_second_name, company_email, full_company_name,
        short_company_name, company_address, company_cell, company_phone, company_site
    )
    region = company_inn[:2]

    if get_main_all:
        kol_rab = get_main_all[0]
        sum_dohod2018 = get_main_all[1]
        sum_rashod2018 = get_main_all[2]
        main_okved_desc = get_main_all[3]
        main_okved_num = get_main_all[4]
        if len(main_okved_num) > 5:
            main_okved_num = main_okved_num[:5]
    else:
        return None

    if not managers:
        print("no managers")
        return None

    approved_managers = []

    for manager in managers:
        manager_vacation = manager[2]
        manager_regions = manager[3]
        if manager_regions == "all":
            manager_regions = region
        manager_okveds = manager[4]

        if (
                manager_regions.find(region) != -1
        ) and (manager_okveds.find(main_okved_num) != -1) and main_okved_num and manager_vacation != "yes":
            approved_managers.append(manager)

    if not approved_managers:
        # print("Didn't get any matches with correct OKVED and correct region===============================")
        for manager in managers:
            manager_vacation = manager[2]
            manager_regions = manager[3]
            if manager_regions == "all":
                manager_regions = region
            manager_okveds = manager[4]
            if not manager_okveds:
                manager_okveds = main_okved_num

            if (manager_regions.find(region) != -1) and (
                    manager_okveds.find(main_okved_num) != -1) and main_okved_num and manager_vacation != "yes":
                approved_managers.append(manager)

    # print(approved_managers, "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    chosen_manager = ""
    manager_email = ""
    if approved_managers:
        len_approved_managers = len(approved_managers)
        # print("Всего подходящих менеджеров на члена ЕРУЗ: ", str(len_approved_managers))
        len_approved_managers_minus_one = len_approved_managers - 1
        chosen_manager_num = random.randint(0, len_approved_managers_minus_one)
        chosen_manager = approved_managers[chosen_manager_num]
        # print("Избранный менеджер: ")
        # print(chosen_manager)
    else:
        print("no approved managers")
        print("")
        print("")
        print("")
        manager_email = "marketing@expertcentre.org"

    if chosen_manager or manager_email:
        try:
            manager_email = chosen_manager[0]
        except Exception:
            manager_email = "marketing@expertcentre.org"

        current_user_bitrix_id = ""
        api_request_current_user = ""

        try:
            api_request_current_user = bx_24.callMethod(
                'user.get',
                filter={'EMAIL': manager_email},
                select=['ID']
            )
        except Exception as message:
            print(message)
        except:
            print("no api request current user")
            print("")
            print("")
            print("")

        if api_request_current_user:
            api_request_current_user = api_request_current_user[0]
            # print(api_request_current_user)
            current_user_bitrix_id = api_request_current_user["ID"]

        if current_user_bitrix_id:
            # status_id = "DETAILS"
            status_id = "2"
            if not company_phone and company_cell:
                company_phone = company_cell
            if not full_company_name:
                full_company_name = short_company_name
            created_by_id = 104

            source_description = "UltraERUZ"
            comment = ""
            main_okved_line = ""
            try:
                add_info = "Среднесписочное количество рабочих в 2018 г: {}. Сумма доходов и расходов в 2018 г. {} {}".format(
                    kol_rab, sum_dohod2018, sum_rashod2018
                )
            except:
                add_info = ""
            if tip_uchastnika == 3:
                title = "Новый член единого реестра участников закупок ИП " + boss_last_name
                boss_title = "ИП"
                comment = "Физическое лицо РФ (индивидуальный предприниматель) {}. Основной вид деятельности: {} {} {} {} {}".format(
                    boss_full_name, main_okved_desc, main_okved_num, eruz_member_link, add_info, company_site
                )
            else:
                title = "Новый член единого реестра участников закупок " + full_company_name

                if main_okved_desc:
                    main_okved_line = "Основной вид деятельности: " + main_okved_desc + " " + main_okved_num + ". "
                else:
                    main_okved_line = "Основной вид деятельности не определен. "

                comment = boss_title + " " + boss_full_name + ". " + main_okved_line + eruz_member_link + add_info + " " + company_site
            try:
                bx_24.callMethod(
                    'crm.lead.add',
                    fields={
                        'TITLE': title,
                        'ASSIGNED_BY_ID': current_user_bitrix_id,
                        'CREATED_BY_ID': created_by_id,
                        'SOURCE_DESCRIPTION': source_description,
                        'EMAIL': [
                            {
                                'VALUE': company_email,
                                'VALUE_TYPE': 'WORK'
                            }
                        ],
                        'STATUS_ID': status_id,
                        'PHONE': [
                            {
                                'VALUE': company_phone,
                                'VALUE_TYPE': 'WORK'
                            }
                        ],
                        'ADDRESS': company_address,
                        'COMMENTS': comment,
                        'COMPANY_TITLE': short_company_name,
                        'UF_CRM_INN': company_inn,
                        'POST': boss_title,
                        'UF_CRM_1593426988': cased_names_one,
                        'UF_CRM_1593426954': cased_names_two,
                        'UF_CRM_1582921386': main_okved_num,
                        'UF_CRM_1586428719': main_okved_desc,
                        'NAME': boss_first_name,
                        'LAST_NAME': boss_last_name,
                        'SECOND_NAME': boss_second_name
                    }
                )
                print("Успешно дали лид " + manager_email)
                print("")
                print("")
                print("")
                print("")

            except Exception:
                print(message)
                print("Лид не раздался по вине Битрикса ((((((((((((((((((((((((")
                print("")
                print("")
            except:
                print("Лид не раздался ((((((((((((((((((((((((")
                print("")
                print("")

    return None


#########END FUNCTION ASSIGNS LEAD TO MANAGER


# assignLead(bx24, companyINN, getMainAll, managers, eruzMemberLink, eruz_registry_date, nalogRegDate, tipUchastnika,
#            bossTitle, bossFullName, bossLastName, bossFirstName, bossSecondName, companyEmail, fullCompanyName,
#            shortCompanyName, companyAddress, companyCell, companyPhone, companySite, casedNamesOne, casedNamesTwo)

print(bx24.get_all('crm.product.list'))
