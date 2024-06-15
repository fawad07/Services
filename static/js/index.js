import { Card } from "../components/Card.js";
import { FormValidator } from "../components/FormValidator.js";
import { Popup } from "../components/Popup.js";
import { PopupWithForm } from "../components/PopupWithForm.js";
import { PopupWithImage } from "../components/PopupWithImage.js";
import { Section } from "../components/Section.js";
import { UserInfo } from "../components/UserInfo.js";
import utils from "../Utils/Constants.js";
import "../pages/index.css";

/*----------------------------------------------------------*/
/*               			FUNCTIONS		                */
/*----------------------------------------------------------*/

/**
 * Param: cardData
 * Description:	card Data is used that is passed to the Image form for display
 */
//Card Image Preview
function handleImageClick(cardData) {
	imagePopup.open(cardData);
} //end func

/**
 * param: data
 * Description:	Takes a data object that is used to create a card with the Card object
 * 						Card Element is created and passed along to the Section object
 * 						Section object visually puts the card on the screen
 */
//func to make new card
function createCard(data) {
	const newCard = new Card(
		data,
		utils.htmlIds.cardTemplate,
		handleImageClick
	); //pass new info to new card
	const elementCard = newCard.getCard();
	sectionCards.addItems(elementCard);
} //end func

/**
 * Param: settings/configurations
 * Description: all form validation initialize
 */
function validateForms(opts) {
	//initialize forms
	const forms = document.querySelectorAll(utils.config.formSelector);
	const formArray = Array.from(forms);
	formArray.forEach((form) => {
		const validateForm = new FormValidator(opts, form);
		validateForm.enableValidation();
	});
} //end func

/**
 * Param: userData
 * Description:	Sets the change/edit name/title and the description of the profile
 */
function handleProfileSubmitForm(userData) {
	userInfo.setUserInfo({
		name: userData.title,
		description: userData.description,
	});
	profileEditForm.close();
} //end func

/**
 * Description:	Adds a new card everytime the + button is clicked
 */
function handleAddCardSubmitForm() {
	//add new card i.e. Create Card
	const name = utils.newCardTitleInput.value; //newCardTitleValue
	const link = utils.newCardUrlInput.value; //newCardUrlValue
	const dataCard = { name, link }; //collect new card data and link
	createCard(dataCard);

	//close addCardPopup
	addCardForm.close();
} //end func

/********************INSTANISATIONS BELOW******************** */

//ALL FORMS VALIDATIONS
validateForms(utils.config);

//CARD SECTION
const sectionCards = new Section(
	{
		items: utils.initialCards,
		renderer: createCard,
	},
	utils.htmlIds.cardList
);
sectionCards.renderItems();

//POP UP WITH IMAGE
const imagePopup = new PopupWithImage(utils.htmlIds.imagePreviewPopup);
imagePopup.setEventListeners();

//EDIT PROFILE FORM
const profileEditForm = new PopupWithForm(
	utils.htmlIds.profileEditPopup,
	handleProfileSubmitForm
);
profileEditForm.setEventListeners();

utils.profileEditButton.addEventListener("click", () => {
	const currentUser = userInfo.getUserInfo();
	utils.profileTitleInput.value = currentUser.name;
	utils.profileDescriptionInput.value = currentUser.description;
	profileEditForm.open();
});

//USER INFO
const userInfo = new UserInfo({
	titleSelector: utils.htmlIds.profileTitle,
	descriptionSelector: utils.htmlIds.profileDescription,
});

//ADD CARD FORM
const addCardForm = new PopupWithForm(
	utils.htmlIds.addCardPopup,
	handleAddCardSubmitForm
);
addCardForm.setEventListeners();

utils.profileAddCardButton.addEventListener("click", () => {
	addCardForm.open();
});
