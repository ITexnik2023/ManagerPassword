from aiogram import Router, types
from services.databases import search_services, get_user_id
from handlers.keyboards import back_kb, main_menu
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class SearchState(StatesGroup):
    waiting_for_service_name = State()

@router.message(lambda message: message.text == "Назад")
async def back_menu(message: types.Message, state: FSMContext):
    current_state = await state.get_data()
    if current_state is None:
        await message.answer("Выберите действие", reply_markup=main_menu())
        return
    await state.clear()
    await message.answer("Выберите действие", reply_markup=main_menu())
@router.message(lambda message: message.text == "Найти сервис")
async def start_search_service(message: types.Message, state: FSMContext):
    username = message.from_user.username
    user_id = get_user_id(username)
    if not user_id:
        await message.answer("❌ Пользователь не найден. Сначала зарегистрируйтесь!", reply_markup=back_kb())
        return
    await state.update_data(user_id=user_id)
    await state.set_state(SearchState.waiting_for_service_name)
    await message.answer("Введите название сервиса!", reply_markup=back_kb())


@router.message(SearchState.waiting_for_service_name)
async def procces_search_service(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await back_menu(message, state)
        return
    data = await state.get_data()
    user_id = data.get("user_id")
    name_service = message.text

    search_result = search_services(user_id, name_service)
    if not search_result:
        await message.answer("Совпадений не найдено", reply_markup=back_kb())
        return

    response = "📁 Найдены следующие совпадения:\n\n" + "\n".join(
        f"🔹 {service[0]} (логин: {service[1]})"
        for service in search_result
    )
    await message.answer(response, reply_markup=back_kb())
    await state.clear()