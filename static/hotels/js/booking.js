// const hotelId = Number(document.getElementsByClassName("hotel-id")[0].value);
var bookingTotal = document.getElementsByClassName("text-main absolute-right");

const form = document.getElementsByClassName("payment-form-wrapper")[0];

var checkoutTotalDOM = document.getElementsByClassName("checkoutTotal");
const checkoutSlug =
  "/hotels/hotel-room-checkout/" === window.location.pathname;
const currentUrl = window.location;
var checkoutItemsPrice = document.getElementsByClassName(
  "hotel-room-sm-item mb-30"
)[0];
if (checkoutSlug) {
  var company_name = document.getElementById("company_name");
  var f_name = document.getElementById("f_name");
  var l_name = document.getElementById("l_name");
  var m_phone = document.getElementById("m_phone");
  var email = document.getElementById("email");
  var password1 = document.getElementById("password1");
  var password2 = document.getElementById("password2");
  var form_message = document.getElementById("form_message");
}

var checkoutItemsDOM = document.getElementsByClassName("checkoutTotal")[0];

const slug =
  currentUrl.href.split("/").pop().split(";")[0] &&
  currentUrl.href.includes("/hotels/");
const villaslug =
  currentUrl.href.split("/").pop().split(";")[0] &&
  currentUrl.href.includes("/apartments/");
const conference_slug =
  currentUrl.href.split("/").pop().split(";")[0] &&
  currentUrl.href.includes("/conference/");
const bookingSlug = slug || villaslug || conference_slug;

if (bookingSlug) {
  var clearBookings = document.getElementsByName("clear-bookings");
  var checkoutBtn = document.getElementById("checkout");
  var bookingItemsDOM = document.getElementsByClassName(
    "hotel-room-sm-item"
  )[0];

  var roomsDOM = document.getElementsByClassName("room-item");

  var stayDuration = Number(
    document.getElementsByClassName("stayduration")[0].value
  );
  // console.log(stayDuration);
  var hotelAddress = document.getElementsByClassName("address-info")[0].value;
  var checkinDate = document.getElementById("dateStart-general").value;
  var checkoutDate = document.getElementById("dateEnd-general").value;
  var hotelId = document.getElementById("hotel-id").value;
}

let bookings = [];
let bookRoomBtnsDOM = [];
let checkoutTotal = 0;
let user = 0;
let hotel_id = 0;
let payStatus = 1;
let passw = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;

//get rooms from database
class Rooms {
  async getRooms() {
    if (bookingSlug) {
      try {
        let results = await fetch(`/api/hotel-room/${hotelId}/`);
        let data = await results.json();
        return data;
      } catch (error) {
        console.log(error);
      }
    }
  }
}

//display booking items
class UI {
  getBookRoomButtons() {
    const bookRoomBtns = [
      ...document.getElementsByClassName("btn btn-primary btn-sm btn-block"),
    ];

    bookRoomBtnsDOM = bookRoomBtns;

    bookRoomBtns.forEach((button) => {
      let id = parseInt(button.dataset.id);
      let booked = bookings.find((item) => parseInt(item.id) === id);
      if (booked) {
        button.innerText = "Room booked";
        button.disabled = true;
      }
      button.addEventListener("click", (event) => {
        event.target.innerText = "Room booked";
        event.target.disabled = true;
        const room = Storage.getRoomFromStorage(id);

        if (stayDuration === 0) {
          stayDuration = 1;
        }
        const roomQuantity =
          parseInt(document.getElementById("roomQty" + id).value) === 0
            ? 1
            : parseInt(document.getElementById("roomQty" + id).value);
        let bookingRoomItem = {
          stay_duration: stayDuration,
          checkin: moment(new Date(checkinDate)).format("YYYY-MM-DD"),
          checkout: moment(new Date(checkoutDate)).format("YYYY-MM-DD"),
          total_guests: room.is_conference_room
            ? roomQuantity
            : room.max_adults * roomQuantity,
          rooms: room.id,
          id: room.id,
          is_conference_room: room.is_conference_room,
          hotel: room.hotel,
          hotel_name: room.hotel_name,
          room_Name: room.room_Name,
          room_Price: room.room_Price,
          user: parseInt(room.user),
          name: room.room_type_name,
          sub_total: room.room_Price * stayDuration * roomQuantity,
          hotel: parseInt(room.hotel),
          qty: roomQuantity,
          hotelAddress,
        };
        //add room item to booking items
        bookings = [...bookings, bookingRoomItem];
        // bookings.push(bookingRoomItem);

        //save bookings in local storage
        Storage.saveBookingstoLocalStorage(bookings);
        //set booking value
        this.setBookingValues(bookings);
        //display booking items
        this.addHotelToBookingItems(bookingRoomItem);
        this.addRoomToBookingItems(bookingRoomItem);
        if (checkoutSlug) {
          this.addCheckoutPrice();
          this.addCheckoutPriceItems(bookingRoomItem);
        }

        // this.setupAPP()
      });
    });
  }
  setBookingValues(bookings) {
    let tempTotal = 0;
    let itemsTotal = 0;
    bookings.map((item) => {
      tempTotal += item.room_Price * item.stay_duration * item.qty;
      itemsTotal += item.qty;
      user = item.user;
      hotel_id = item.hotel;
    });
    Storage.saveTotalToLocalStorage(tempTotal);
    Storage.saveUserToLocalStorage(user);
    Storage.saveHotelIdToLocalStorage(hotel_id);
    if (checkoutSlug) {
      // bookingTotal[0].innerText = parseFloat(tempTotal.toFixed(2));
      // Storage.saveTotalToLocalStorage(tempTotal);
    }
  }

  addHotelToBookingItems(item) {
    if (bookingSlug) {
      var hotelName = document.getElementsByClassName("name")[0].innerText;
    }
    var currentHotelItems = document.getElementsByClassName(
      "hotel-room-sm-item"
    )[0];
    var currentHotelNames = currentHotelItems.getElementsByClassName(
      "current-hotel-item"
    );
    let bookingHotelItemDiv = document.createElement("div");
    bookingHotelItemDiv.setAttribute("class", "the-hotel-item");

    for (let i = 0; i < currentHotelNames.length; i++) {
      if (currentHotelNames[i].innerText == hotelName) {
        return;
      }
    }
    bookingHotelItemDiv.innerHTML = `
    <h5><a href="#" data-id=${item.id} id='hotel${item.id}' class='current-hotel-item'>${item.hotel_name}</a></h5>
    <div class="d-flex">
        <div>
            <p class="location">${item.hotelAddress}</p>
        </div>
    `;
    if (bookingSlug) {
      bookingItemsDOM.appendChild(bookingHotelItemDiv);
    }
  }

  addRoomToBookingItems(item) {
    var bookingRoomItemDiv = document.createElement("div");
    bookingRoomItemDiv.setAttribute("class", "the-room-item");

    bookingRoomItemDiv.innerHTML = `
    <h6 class='room-title'>${item.room_Name}</h6>
    <div class="clearfix">
        <span class="amount"> ${item.stay_duration} ${
      item.is_conference_room ? "Days" : "Nights"
    } x ${item.qty} ${item.is_conference_room ? "Guests" : "Rooms"}</span>
        <span class="price">Ksh ${item.room_Price} </span>
    </div>
    <a href="javascript:void(0)" class="remove" data-id=${
      item.id
    }><i class="fa fa-times"></i></a>
    `;

    if (bookingSlug) {
      bookingItemsDOM.appendChild(bookingRoomItemDiv);
    }

    this.checkout();
  }

  addCheckoutRoomItems(item) {
    if (checkoutSlug) {
      var bookingRoomItemDivCheckout = document.createElement("div");
      bookingRoomItemDivCheckout.setAttribute("class", "the-room-item");
      bookingRoomItemDivCheckout.innerHTML = `
      <h6 class='room-title'>${item.room_Name}</h6>
      <div class="clearfix">
          <span class="amount"> ${item.stay_duration} ${
        item.is_conference_room ? "Days" : "Nights"
      } x ${item.qty} ${item.is_conference_room ? "Guest(s)" : "Room(s)"}</span>
          <span class="price">Ksh ${this.formatNumber(
            item.room_Price * item.stay_duration * parseInt(item.qty)
          )} </span>
      </div>
      `;
      checkoutItemsPrice.appendChild(bookingRoomItemDivCheckout);
    }
  }

  addCheckoutPriceItems() {
    if (checkoutSlug) {
      var bookingRoomItemUL = document.createElement("ul");
      bookingRoomItemUL.setAttribute("class", "summary-price-list");
      bookingRoomItemUL.innerHTML = `
        <li>Sub total <span class="absolute-right">Ksh ${this.formatNumber(
          checkoutTotal
        )}</span></li>
        <li>taxes and fees <span class="absolute-right">Ksh${0}</span></li>
        <li class="total">Total <span class="text-main absolute-right">Ksh ${this.formatNumber(
          checkoutTotal
        )}</span></li>
      `;
      checkoutItemsDOM.appendChild(bookingRoomItemUL);
    }
  }

  setupAPP() {
    bookings = Storage.getBookings();
    checkoutTotal = parseFloat(Storage.getCheckoutTotal()).toFixed(2);
    user = parseInt(Storage.getUser());
    hotel_id = Storage.getHotelId();
    this.setBookingValues(bookings);
    this.populateBookings(bookings);
  }
  checkout() {
    if (bookingSlug) {
      if (bookings.length === 0) {
        checkoutBtn.disabled = true;
      } else {
        checkoutBtn.disabled = false;
        checkoutBtn.addEventListener("click", () => {
          window.location.replace("/hotels/hotel-room-checkout/");
          // location.pathname = "/hotels/hotel-room-checkout/";
        });
      }
    }
  }

  formatNumber(num) {
    return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
  }

  populateBookings(bookings) {
    this.addCheckoutPriceItems();
    this.checkout();
    bookings.forEach((item) => {
      this.addHotelToBookingItems(item);
      this.addRoomToBookingItems(item);
      this.addCheckoutRoomItems(item);
    });
  }
  verifyFormInputs() {
    const f_nameValue = f_name.value.trim();
    const l_nameValue = l_name.value.trim();
    const m_phoneValue = m_phone.value.trim();
    const emailValue = email.value.trim();

    if (document.getElementById("createAccountCheckBox").checked) {
      var password1Value = password1.value.trim();
      var password2Value = password2.value.trim();
    }

    if (f_nameValue === "") {
      this.setErrorMsgFor(f_name, "First name should not be empty");
      var verified = false;
    } else {
      this.setSuccessMsgFor(f_name);
      var verified = true;
    }

    if (l_nameValue === "") {
      this.setErrorMsgFor(l_name, "Last name should not be empty");
      var verified = false;
    } else {
      this.setSuccessMsgFor(l_name);
      var verified = true;
    }

    if (m_phoneValue === "") {
      this.setErrorMsgFor(m_phone, "Mobile phone should not be empty");
      var verified = false;
    } else {
      this.setSuccessMsgFor(m_phone);
      var verified = true;
    }

    // if (company_nameValue === "") {
    //   this.setErrorMsgFor(company_name, "Company name should not be empty");
    // } else {
    //   this.setSuccessMsgFor(company_name);
    // }

    if (emailValue === "") {
      this.setErrorMsgFor(email, "Email cannot be blank");
      var verified = false;
    } else if (!this.isEmail(emailValue)) {
      this.setErrorMsgFor(email, "Not a valid email");
      var verified = false;
    } else {
      this.setSuccessMsgFor(email);
      var verified = true;
    }

    if (document.getElementById("createAccountCheckBox").checked) {
      if (password1Value === "") {
        this.setErrorMsgFor(password1, "Password cannot be blank");
        var verified = false;
      } else {
        this.setSuccessMsgFor(password1);
        var verified = true;
      }
      if (password2Value === "") {
        this.setErrorMsgFor(password2, "Password2 cannot be blank");
        var verified = false;
      } else if (password1Value !== password2Value) {
        this.setErrorMsgFor(password2, "Passwords do not match");
        var verified = false;
      } else if (!password2Value.match(passw)) {
        this.setErrorMsgFor(
          password2,
          "6 characters with a digit, lower and uppercase letters"
        );
        var verified = false;
      } else {
        this.setSuccessMsgFor(password2);
        var verified = true;
      }
    }

    return verified;
  }

  setErrorMsgFor(input, message) {
    const formGroup = input.parentElement;
    const small = formGroup.querySelector("small");
    formGroup.className = "form-group error";
    small.innerText = message;
  }

  setSuccessMsgFor(input) {
    const formGroup = input.parentElement;
    formGroup.className = "form-group success";
  }

  checkPassword(inputtxt) {
    let passw = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;
    if (inputtxt.value.match(passw)) {
      return true;
    } else {
      alert("Wrong...!");
      return false;
    }
  }

  isEmail(email) {
    return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
      email
    );
  }
  bookingLogic() {
    //clear booking items
    if (bookingSlug) {
      console.log("here");
      clearBookings[0].addEventListener("click", () => {
        this.resetBookings();
        this.checkout();
      });

      //remove single booking item
      bookingItemsDOM.addEventListener("click", (event) => {
        if (event.target.parentElement.classList.contains("remove")) {
          console.log("running...");
          let removeItem = event.target.parentElement;
          var roomId = parseInt(removeItem.dataset.id);
          bookingItemsDOM.removeChild(removeItem.parentElement);
          const hotelDiv = document.getElementById("hotel" + roomId);
          if (hotelDiv != null) {
            bookingItemsDOM.removeChild(hotelDiv.parentElement.parentElement);
          }

          this.removeItem(roomId);
        }
      });
      this.checkout();
    }

    if (checkoutSlug) {
      if (bookings.length === 0) {
        window.location.replace("/hotels/");
      }
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        this.verifyFormInputs();
        console.log("inputs");
        if (document.getElementById("paymentOptionPaypal").checked) {
          payStatus = 3;
        }
        const f_nameValue = f_name.value.trim();
        const l_nameValue = l_name.value.trim();
        const m_phoneValue = m_phone.value.trim();
        const emailValue = email.value.trim();
        const form_messageValue = form_message.value.trim();
        const company_nameValue = (company_name || {}).value || "N/A";
        if (document.getElementById("createAccountCheckBox").checked) {
          var password2Value = password2.value.trim();
        }

        var userData = [
          { name: f_nameValue + " " + l_nameValue },
          { email: emailValue },
          { parent: parseInt(user) },
          { password: password2Value },
          { from_api: false },
        ];

        var checkoutData = {
          guest_name: f_nameValue + " " + l_nameValue,
          mobile_Number: m_phoneValue,
          email: emailValue,
          company_name: company_nameValue,
          hotel: parseInt(hotel_id),
          items: bookings,
          user: parseInt(user),
          final_total: parseInt(checkoutTotal),
          special_requests: form_messageValue,
          payment_option: payStatus,
        };
        if (password2Value) {
          console.log(password2Value);
          checkoutData = { ...checkoutData, account: userData };
        } else {
          checkoutData = { ...checkoutData };
        }

        if (this.verifyFormInputs()) {
          this.disableBookingBtn();
          await this.addBooking(checkoutData);
          window.location.replace("/hotels/booking/success/");
          localStorage.clear();
        } else {
          alert("You have errors on the form. Please correct to proceed");
        }
      });
    }
  }

  disableBookingBtn() {
    const bookingBtn = document.querySelector("#complete-booking");
    bookingBtn.disabled = true;
  }

  addBooking = async (checkoutData) => {
    try {
      await axios.post(`/api/booking/new/`, checkoutData);
    } catch (error) {
      console.log(error);
    }
  };

  resetBookings() {
    if (bookingSlug) {
      let bookingItems = bookings.map((item) => item.id);
      bookingItems.forEach((id) => this.removeItem(id));
      while (bookingItemsDOM.children.length > 0) {
        bookingItemsDOM.removeChild(bookingItemsDOM.children[0]);
      }
      // this.checkout();
    }
  }
  removeItem(id) {
    bookings = bookings.filter((item) => item.id !== id);
    this.setBookingValues(bookings);
    Storage.saveBookingstoLocalStorage(bookings);
    let button = this.getSingleButton(id);
    button.disabled = false;
    button.innerText = "book";
    this.checkout();
  }
  getSingleButton(id) {
    return bookRoomBtnsDOM.find((button) => parseInt(button.dataset.id) === id);
  }
}
//local storage setup
class Storage {
  static saveRoomsToStorage(roomsData) {
    localStorage.setItem("roomsData", JSON.stringify(roomsData));
  }
  static getRoomFromStorage(id) {
    let roomsData = JSON.parse(localStorage.getItem("roomsData"));
    return roomsData.find((room) => room.id === id);
  }
  static saveBookingstoLocalStorage(bookings) {
    localStorage.setItem("bookings", JSON.stringify(bookings));
  }
  static saveTotalToLocalStorage(checkoutTotal) {
    localStorage.setItem("checkoutTotal", JSON.stringify(checkoutTotal));
  }
  static saveUserToLocalStorage(user) {
    localStorage.setItem("user", JSON.stringify(user));
  }
  static saveHotelIdToLocalStorage(hotel_id) {
    localStorage.setItem("hotel_id", JSON.stringify(hotel_id));
  }

  static getCheckoutTotal() {
    return localStorage.getItem("checkoutTotal");
  }
  static getUser() {
    return localStorage.getItem("user");
  }
  static getHotelId() {
    return localStorage.getItem("hotel_id");
  }
  static getBookings() {
    return localStorage.getItem("bookings")
      ? JSON.parse(localStorage.getItem("bookings"))
      : [];
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const ui = new UI();
  const roomsData = new Rooms();
  ui.setupAPP();
  //get all rooms for specific hotel
  roomsData
    .getRooms()
    .then((roomsData) => {
      Storage.saveRoomsToStorage(roomsData);
    })
    .then(() => {
      ui.getBookRoomButtons();
      ui.bookingLogic();
    });
});
