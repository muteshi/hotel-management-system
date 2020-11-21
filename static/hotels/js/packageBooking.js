// const hotelId = Number(document.getElementsByClassName("hotel-id")[0].value);
var bookingTotal = document.getElementsByClassName("text-main absolute-right");

var checkoutTotalDOM = document.getElementsByClassName("checkoutTotal");
const checkoutSlug =
  "/packages/hotel-package-checkout/" === window.location.pathname;
const currentUrl = window.location;
var checkoutItemsPrice = document.getElementsByClassName(
  "hotel-room-sm-item mb-30"
)[0];
var checkoutItemsDOM = document.getElementsByClassName("checkoutTotal")[0];
if (checkoutSlug) {
  var form = document.getElementsByClassName("payment-form-wrapper")[0];
  var company_name = document.getElementById("company_name");
  var f_name = document.getElementById("f_name");
  var l_name = document.getElementById("l_name");
  var m_phone = document.getElementById("m_phone");
  var email = document.getElementById("email");
  var password1 = document.getElementById("password1");
  var password2 = document.getElementById("password2");
  var form_message = document.getElementById("form_message");
}
const bookingSlug =
  currentUrl.href.split("/").pop().split(";")[0] &&
  currentUrl.href.includes("/hotels/packages/");

if (bookingSlug) {
  var clearBookings = document.getElementsByName("clear-bookings");
  var checkoutBtn = document.getElementById("checkout");
  var bookingItemsDOM = document.getElementsByClassName(
    "hotel-room-sm-item"
  )[0];

  var roomsDOM = document.getElementsByClassName("room-item");

  // console.log(stayDuration);
  var hotelAddress = document.getElementsByClassName("address-info")[0].value;

  var packageId = document.getElementById("package-id").value;
}

let bookings = [];
let bookpackageBtnsDOM = [];
let checkoutTotal = 0;
let user = 0;
let package_id = 0;
let payStatus = 1;
let passw = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;

//get rooms from database
class Packages {
  async getHotelPackages() {
    if (bookingSlug) {
      try {
        let results = await fetch(`/api/hotelpackages/${packageId}/`);
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
  getBookPackageButtons() {
    const bookPackageBtns = [
      ...document.getElementsByClassName("btn btn-primary btn-sm btn-block"),
    ];

    bookpackageBtnsDOM = bookPackageBtns;

    bookPackageBtns.forEach((button) => {
      let id = parseInt(button.dataset.id);
      let booked = bookings.find((item) => parseInt(item.id) === id);

      if (booked) {
        button.innerText = "Hotel booked";
        button.disabled = true;
      }
      button.addEventListener("click", (event) => {
        event.target.innerText = "Hotel booked";
        event.target.disabled = true;
        const hotel = Storage.getHotelPackageFromStorage(id);

        var checkinDateDOM = document.getElementsByName(
          "dateStart-general" + id
        )[0];
        var defaultCheckinDate = new Date(
          checkinDateDOM.defaultValue ? checkinDateDOM.defaultValue : new Date()
        );
        var currentCheckinDate = new Date(
          checkinDateDOM.value ? checkinDateDOM.value : new Date()
        );

        const guestQuantity =
          parseInt(document.getElementById("guestQty" + id).value) === 0
            ? 1
            : parseInt(document.getElementById("guestQty" + id).value);

        const stayDuration = parseInt(
          document.getElementById("stayduration" + id).value
        );

        if (defaultCheckinDate !== currentCheckinDate) {
          var checkinDate = currentCheckinDate;
        } else {
          checkinDate = defaultCheckinDate;
        }
        checkinDate = moment(checkinDate).format("YYYY-MM-DD");

        const checkoutDate = moment(checkinDate, "YYYY-MM-DD").add(
          stayDuration,
          "days"
        );

        let bookingRoomItem = {
          stay_duration: stayDuration,
          checkin: checkinDate,
          checkout: moment(new Date(checkoutDate)).format("YYYY-MM-DD"),
          total_guests: guestQuantity,
          hotel_package: hotel.id,
          id: hotel.id,
          hotel_name: hotel.hotel_name,
          package_Price: hotel.package_Price,
          user: parseInt(hotel.hotel_user),
          name: hotel.package_name,
          sub_total: hotel.package_Price * guestQuantity * stayDuration,
          package: parseInt(hotel.package),
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
        this.addHotelPackageToBookingItems(bookingRoomItem);
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
    bookings.map((item) => {
      tempTotal += item.package_Price * item.total_guests * item.stay_duration;
      user = item.user;
      package_id = item.package;
    });
    Storage.saveTotalToLocalStorage(tempTotal);
    Storage.saveUserToLocalStorage(user);
    Storage.savePackageIdToLocalStorage(package_id);
  }

  addHotelPackageToBookingItems(item) {
    var bookingHotelPackageItemDiv = document.createElement("div");
    bookingHotelPackageItemDiv.setAttribute("class", "the-room-item");

    bookingHotelPackageItemDiv.innerHTML = `
    <h6 class='room-title'>${item.name} in ${item.hotel_name} (${
      item.stay_duration
    } night stay)</h6>
    <div class="clearfix">
        <span class="amount"> ${item.total_guests} persons
    x ${item.package_Price} </span>
        <span class="price">Ksh ${this.formatNumber(
          item.package_Price * item.total_guests * item.stay_duration
        )} </span>
    </div>
    <a href="javascript:void(0)" class="remove" data-id=${
      item.id
    }><i class="fa fa-times"></i></a>
    `;

    if (bookingSlug) {
      bookingItemsDOM.appendChild(bookingHotelPackageItemDiv);
    }

    this.checkout();
  }

  addCheckoutHotelPackageItems(item) {
    if (checkoutSlug) {
      var bookingHotelPackageItemDivCheckout = document.createElement("div");
      bookingHotelPackageItemDivCheckout.setAttribute("class", "the-room-item");
      bookingHotelPackageItemDivCheckout.innerHTML = `
      <h6 class='room-title'>${item.name} in ${item.hotel_name} for ${
        item.stay_duration
      } night stay</h6>
      <div class="clearfix">
          
          <span class="price">Ksh ${this.formatNumber(
            item.package_Price * item.total_guests
          )} </span>
      </div>
      `;
      checkoutItemsPrice.appendChild(bookingHotelPackageItemDivCheckout);
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
    package_id = Storage.getHotelId();
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
          location.pathname = "/packages/hotel-package-checkout/";
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
      this.addHotelPackageToBookingItems(item);
      this.addCheckoutHotelPackageItems(item);
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
          package: parseInt(package_id),
          items: bookings,
          user: parseInt(user),
          final_total: parseInt(checkoutTotal),
          special_requests: form_messageValue,
          payment_option: payStatus,
        };
        if (password2Value) {
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
    return bookpackageBtnsDOM.find(
      (button) => parseInt(button.dataset.id) === id
    );
  }
}
//local storage setup
class Storage {
  static saveHotelPackagesToStorage(packageData) {
    localStorage.setItem("packageData", JSON.stringify(packageData));
  }
  static getHotelPackageFromStorage(id) {
    let packageData = JSON.parse(localStorage.getItem("packageData"));
    return packageData.find((room) => room.id === id);
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
  static savePackageIdToLocalStorage(package_id) {
    localStorage.setItem("package_id", JSON.stringify(package_id));
  }

  static getCheckoutTotal() {
    return localStorage.getItem("checkoutTotal");
  }
  static getUser() {
    return localStorage.getItem("user");
  }
  static getHotelId() {
    return localStorage.getItem("package_id");
  }
  static getBookings() {
    return localStorage.getItem("bookings")
      ? JSON.parse(localStorage.getItem("bookings"))
      : [];
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const ui = new UI();
  const packages = new Packages();
  ui.setupAPP();
  //get all rooms for specific hotel
  packages
    .getHotelPackages()
    .then((packages) => {
      Storage.saveHotelPackagesToStorage(packages);
    })
    .then(() => {
      ui.getBookPackageButtons();
      ui.bookingLogic();
    });
});
