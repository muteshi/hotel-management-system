if (document.readyState == "loading") {
  document.addEventListener("DOMContentLoaded", ready);
} else {
  ready();
}

function ready() {
  let removedRoomItems = document.getElementsByClassName("remove");
  for (let i = 0; i < removedRoomItems.length; i++) {
    var room = removedRoomItems[i];
    room.addEventListener("click", removeRoomItem);
  }
}

let bookings = document.getElementsByClassName(
  "btn btn-primary btn-sm btn-block"
);

// let bookRoomButtons = document.getElementsByClassName(
//   "btn btn-primary btn-sm btn-block"
// );

async function getHotelRooms(hotelId) {
  let response = await fetch(`/api/hotel-room/${hotelId}/`);
  let rooms = await response.json();
  return rooms;
}

const hotelId = Number(document.getElementsByClassName("hotel-id")[0].value);

for (let index = 0; index < bookings.length; index++) {
  bookings[index].addEventListener("click", () => {
    getHotelRooms(hotelId).then((rooms) => bookingRoomItems(rooms[index]));
  });
}

function bookingRoomItems(room) {
  let bookingItems = localStorage.getItem("bookingItems");
  bookingItems = JSON.parse(bookingItems);
  if (bookingItems != null) {
    if (bookingItems[room.slug] === undefined) {
      bookingItems = {
        ...bookingItems,
        [room.slug]: room,
      };
    } else {
      bookingItems = {
        ...bookingItems,
        [room.slug]: room,
      };
    }
  } else {
    bookingItems = {
      [room.slug]: room,
    };
  }
  localStorage.setItem("bookingItems", JSON.stringify(bookingItems));
}

console.log(bookings);
// function displayBookingItems() {
//   let bookingItems = localStorage.getItem("bookingItems")
//   let hotelAddress = document.getElementsByClassName("address-info")[0].value
//   // let bookingItems = document.getElementsByClassName("hotel-room-sm-item")[0];
//   bookingItems = JSON.parse(bookingItems)
//   let bookingItemsDiv = document.getElementsByClassName("hotel-room-sm-item")[0];
//   if (bookingItems && bookingItemsDiv) {
//     bookingItemsDiv.innerHTML = ''
//     Object.values(bookingItems).map(item => {
//       console.log(bookingItems[item.hotel_slug]);
//       bookingItemsDiv.innerHTML += `
//       <div class="the-hotel-item">
//       <h5><a href="#" class='current-hotel-item'>${bookingItems[item.hotel_slug]}</a></h5>
//     <div class="d-flex">
//         <div>
//             <p class="location">${hotelAddress}</p>
//         </div>
//         </div>
//         <div class="the-room-item">
//         <h6 class='room-title'>${item.room_Name}</h6>
//     <div class="clearfix">
//         <span class="amount"> ${item.id} nights x ${item.id}</span>
//         <span class="price">Ksh ${item.room_Price} </span>
//     </div>
//     <a href="#" class="remove"><i class="fa fa-times"></i></a>
//     </div>
//       `
//     })
//   }
//   console.log(bookingItemsDiv);

// }

for (let i = 0; i < bookings.length; i++) {
  let button = bookings[i];
  button.addEventListener("click", bookRoomButtonClicked);
}

function bookRoomButtonClicked(event) {
  let button = event.target;

  let roomBookingItem =
    button.parentElement.parentElement.parentElement.parentElement;
  console.log(roomBookingItem);
  let roomName = roomBookingItem
    .getElementsByClassName("content")[0]
    .children[0].getElementsByTagName("a")[0].innerText;
  const hotelId = Number(document.getElementsByClassName("hotel-id")[0].value);
  let roomPrice = parseFloat(
    roomBookingItem
      .getElementsByClassName("content")[0]
      .children[3].innerText.replace(/[^0-9]/g, "")
  );
  let roomQty = Number(
    roomBookingItem.getElementsByClassName(
      "form-control touch-spin-03 form-readonly-control"
    )[0].value
  );
  let stayDuration = Number(
    roomBookingItem.getElementsByClassName("stayduration")[0].value
  );

  addBookingHotelItem();
  addBookingItem(roomQty, stayDuration);
}

function addBookingItem(roomQty, stayDuration) {
  let bookingRoomItem = document.createElement("div");
  bookingRoomItem.setAttribute("class", "the-room-item");
  let bookingItems = document.getElementsByClassName("hotel-room-sm-item")[0];

  let currentRoomNames = bookingItems.getElementsByClassName("room-title");

  for (let i = 0; i < currentRoomNames.length; i++) {
    if (currentRoomNames[i].innerText == roomName) {
      alert("You have already added this room!");
      return;
    }
  }

  let bookingLocalStorageItems = localStorage.getItem("bookingItems");

  bookingLocalStorageItems = JSON.parse(bookingLocalStorageItems);

  Object.values(bookingLocalStorageItems).map((item) => {
    let bookingItemContents = `
    <h6 class='room-title'>${item.room_Name}</h6>
    <div class="clearfix">
        <span class="amount"> ${stayDuration} nights x ${roomQty}</span>
        <span class="price">Ksh ${item.room_Price} </span>
    </div>
    <a href="#" class="remove"><i class="fa fa-times"></i></a>
`;
  });

  bookingRoomItem.innerHTML = bookingItemContents;
  bookingItems.append(bookingRoomItem);
  // console.log(bookingItems);
  // sessionStorage.setItem('bookingItems', bookingItems);
  // let data = sessionStorage.getItem('bookingItems')
  // for (let index = 0; index < data.length; index++) {
  //   const element = data[index];
  //   console.log(element);

  // }
}

function addBookingHotelItem() {
  let bookingHotelItem = document.createElement("div");
  bookingHotelItem.setAttribute("class", "the-hotel-item");

  let hotelName = document.getElementsByClassName("name")[0].innerText;
  let hotelAddress = document.getElementsByClassName("address-info")[0].value;
  let bookingItems = document.getElementsByClassName("hotel-room-sm-item")[0];

  let currentHotelItems = document.getElementsByClassName(
    "hotel-room-sm-item"
  )[0];
  let currentHotelNames = currentHotelItems.getElementsByClassName(
    "current-hotel-item"
  );

  for (let i = 0; i < currentHotelNames.length; i++) {
    if (currentHotelNames[i].innerText == hotelName) {
      return;
    }
  }
  let bookingLocalStorageItems = localStorage.getItem("bookingItems");

  bookingLocalStorageItems = JSON.parse(bookingLocalStorageItems);

  Object.values(bookingLocalStorageItems).map((item) => {
    let hotelItemContents = `
    <h5><a href="#" class='current-hotel-item'>${item.hotel_name}</a></h5>
    <div class="d-flex">
        <div>
            <p class="location">${hotelAddress}</p>
        </div>
    `;
  });
  bookingHotelItem.innerHTML = hotelItemContents;
  bookingItems.append(bookingHotelItem);
}

function removeRoomItem(event) {
  let roomClicked = event.target;
  roomClicked.parentElement.parentElement.remove();
  updateBookingTotal();
}

function updateBookingTotal() {
  let roomRows = document.getElementsByClassName("the-room-item");
  console.log(roomRows);
  let roomsTotal = 0;
  for (let i = 0; i < roomRows.length; i++) {
    let roomRow = roomRows[i];
    let priceElement = roomRow.getElementsByClassName("price")[0];
    let qtyElement = roomRow.getElementsByClassName("amount")[0];
    let price = parseFloat(priceElement.innerText.replace("Ksh", ""));
    let nights = Number(qtyElement.innerText.replace(/[^0-9]/g, "").charAt(0));
    let rooms = Number(qtyElement.innerText.replace(/[^0-9]/g, "").charAt(1));
    let qty = nights * rooms;
    let roomTotal = qty * price;
    roomsTotal += roomTotal;
  }
  // document.getElementById('roomsTotal').innerText.replace('$178', roomsTotal);
}

// displayBookingItems()
