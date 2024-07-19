def add_income_or_expenses(user_id, category, type_operations, money, comment, dbase):
    """Функция добавляет в бд доходы/расходы"""
    try:
        money = float(money)
        if money < 0:
            return False
        else:
            dbase.addOperations(user_id, category, type_operations, money, comment)
            return True
    except ValueError:
        return False
