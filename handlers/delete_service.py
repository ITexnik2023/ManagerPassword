from aiogram import Router, types
from services.databases import delete_service, search_services, get_user_id
from handlers.keyboards import back_kb, main_menu
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()


class DeleteState(StatesGroup):
    waiting_for_service_name = State()


@router.message(lambda message: message.text == "Назад")
async def back_menu(message: types.Message, state: FSMContext):
    current_state = await state.get_data()
    if current_state is None:
        await message.answer("Выберите действие", reply_markup=main_menu())
        return
    await state.clear()
    await message.answer("Выберите действие", reply_markup=main_menu())


@router.message(lambda message: message.text == "Удалить сервис")
async def start_delete_service(message: types.Message, state: FSMContext):
    username = message.from_user.username
    user_id = get_user_id(username)
    if not user_id:
        await message.answer("❌ Пользователь не найден. Сначала зарегистрируйтесь!", reply_markup=back_kb())
        return
    await state.update_data(user_id=user_id)
    await state.set_state(DeleteState.waiting_for_service_name)
    await message.answer("Введите название сервиса!", reply_markup=back_kb())


@router.message(DeleteState.waiting_for_service_name)
async def procces_delete_service(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await back_menu(message, state)
        return

    data = await state.get_data()
    user_id = data.get("user_id")
    name_service = message.text

    deleted_count = delete_service(user_id, name_service)

    if deleted_count == 0:
        await message.answer("❌ Совпадений не найдено", reply_markup=back_kb())
    else:
        await message.answer(f"✅ Успешно удалено {deleted_count} записей", reply_markup=back_kb())

    await state.clear()