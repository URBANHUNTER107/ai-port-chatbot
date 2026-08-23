/* ============================================================
   FARHAN.AI — NEW UI JAVASCRIPT
   ============================================================ */


/* ============================================================
   BACKEND
   ============================================================ */

const BACKEND_URL = "/api";


/* ============================================================
   VISITOR IDENTITY
   ============================================================ */

function getOrCreateVisitorId() {

    let id = localStorage.getItem("visitorId");

    if (!id) {
        id = crypto.randomUUID();
        localStorage.setItem("visitorId", id);
    }

    return id;
}

const visitorId = getOrCreateVisitorId();


/* ============================================================
   ELEMENTS
   ============================================================ */

const messagesBox = document.getElementById("messages");
const questionInput = document.getElementById("questionInput");
const sendButton = document.getElementById("sendButton");

const mobileMenuButton =
    document.getElementById("mobileMenuButton");

const mobileMenu =
    document.getElementById("mobileMenu");


/* ============================================================
   USER INITIAL
   ============================================================ */

function getInitial(name) {

    if (!name || !name.trim()) {
        return "Y";
    }

    return name.trim().charAt(0).toUpperCase();
}


/* ============================================================
   ADD CHAT MESSAGE
   ============================================================ */

function addMessage(text, sender) {

    if (!messagesBox) {
        return;
    }


    /* --------------------------------------------------------
       MAIN ROW
       -------------------------------------------------------- */

    const wrapper = document.createElement("div");

    wrapper.classList.add("chat-row");

    if (sender === "user") {
        wrapper.classList.add("row-user");
    } else {
        wrapper.classList.add("row-ai");
    }


    /* --------------------------------------------------------
       AVATAR
       -------------------------------------------------------- */

    const avatar = document.createElement("div");

    avatar.classList.add("avatar");


    /* --------------------------------------------------------
       NAME
       -------------------------------------------------------- */

    const nameLabel = document.createElement("div");

    nameLabel.classList.add("sender-name");


    /* --------------------------------------------------------
       MESSAGE COLUMN
       -------------------------------------------------------- */

    const bubbleColumn = document.createElement("div");

    bubbleColumn.classList.add("bubble-column");


    /* --------------------------------------------------------
       MESSAGE BUBBLE
       -------------------------------------------------------- */

    const message = document.createElement("div");

    message.classList.add("chat-message");

    if (sender === "user") {
        message.classList.add("user-message");
    } else {
        message.classList.add("ai-message");
    }

    message.innerText = text || "";


    /* ========================================================
       USER MESSAGE
       ======================================================== */

    if (sender === "user") {

        const userName =
            localStorage.getItem("visitorName") || "You";


        /* Name */

        nameLabel.innerText = userName;


        /* Initial */

        avatar.innerText = getInitial(userName);


        /* Message column */

        bubbleColumn.appendChild(nameLabel);
        bubbleColumn.appendChild(message);


        /*
           IMPORTANT:

           User message goes to the RIGHT.

           HTML order:
           message + avatar

           CSS will use flex-direction: row-reverse
           for .row-user.
        */

        wrapper.appendChild(bubbleColumn);
        wrapper.appendChild(avatar);

    }


    /* ========================================================
       FARHAN MESSAGE
       ======================================================== */

    else {

        const avatarImage =
            document.createElement("img");


        /*
           Your actual uploaded image is:

           farhan.jpeg
        */

        avatarImage.src = "farhan.jpeg";

        avatarImage.alt = "Farhan";


        avatar.appendChild(avatarImage);


        /* Farhan name */

        nameLabel.innerText = "Farhan";


        /* Message */

        bubbleColumn.appendChild(nameLabel);
        bubbleColumn.appendChild(message);


        /*
           Farhan stays on the LEFT.

           HTML order:
           avatar + message
        */

        wrapper.appendChild(avatar);
        wrapper.appendChild(bubbleColumn);
    }


    /* --------------------------------------------------------
       ADD TO CHAT
       -------------------------------------------------------- */

    messagesBox.appendChild(wrapper);


    /* Always scroll to latest message */

    messagesBox.scrollTop =
        messagesBox.scrollHeight;
}


/* ============================================================
   NAME POPUP
   ============================================================ */

function closeNamePopup() {

    const overlay =
        document.getElementById("nameModalOverlay");


    if (!overlay) {
        return;
    }


    overlay.classList.remove("active");


    document.body.classList.remove("modal-open");
}


/* ============================================================
   SHOW NAME POPUP
   ============================================================ */

function showNamePopupIfFirstVisit() {

    const overlay =
        document.getElementById("nameModalOverlay");


    if (!overlay) {
        return;
    }


    /*
       If the visitor has already answered
       the popup, don't show it again.
    */

    if (
        localStorage.getItem("nameAsked") === "true"
    ) {
        return;
    }


    /* Show popup */

    overlay.classList.add("active");


    document.body.classList.add("modal-open");


    /* --------------------------------------------------------
       ELEMENTS
       -------------------------------------------------------- */

    const nameInput =
        document.getElementById("nameInput");

    const nameSubmit =
        document.getElementById("nameSubmit");

    const nameSkip =
        document.getElementById("nameSkip");


    /* --------------------------------------------------------
       Focus input
       -------------------------------------------------------- */

    if (nameInput) {

        setTimeout(() => {

            nameInput.focus();

        }, 100);
    }


    /* ========================================================
       CONTINUE
       ======================================================== */

    if (
        nameSubmit &&
        !nameSubmit.dataset.bound
    ) {

        nameSubmit.dataset.bound = "true";


        nameSubmit.addEventListener(
            "click",
            () => {

                const name =
                    nameInput
                        ? nameInput.value.trim()
                        : "";


                /*
                   Save name only if
                   the visitor actually entered one.
                */

                if (name) {

                    localStorage.setItem(
                        "visitorName",
                        name
                    );
                }


                /*
                   Remember that popup
                   has already been answered.
                */

                localStorage.setItem(
                    "nameAsked",
                    "true"
                );


                closeNamePopup();
            }
        );
    }


    /* ========================================================
       SKIP
       ======================================================== */

    if (
        nameSkip &&
        !nameSkip.dataset.bound
    ) {

        nameSkip.dataset.bound = "true";


        nameSkip.addEventListener(
            "click",
            () => {

                /*
                   Remove any old name.
                */

                localStorage.removeItem(
                    "visitorName"
                );


                /*
                   Remember that visitor
                   chose to skip.
                */

                localStorage.setItem(
                    "nameAsked",
                    "true"
                );


                closeNamePopup();
            }
        );
    }


    /* ========================================================
       ENTER KEY IN NAME INPUT
       ======================================================== */

    if (
        nameInput &&
        !nameInput.dataset.bound
    ) {

        nameInput.dataset.bound = "true";


        nameInput.addEventListener(
            "keydown",
            (event) => {

                if (event.key === "Enter") {

                    event.preventDefault();

                    if (nameSubmit) {
                        nameSubmit.click();
                    }
                }
            }
        );
    }
}


/* ============================================================
   LOAD CHAT HISTORY
   ============================================================ */

async function loadHistory() {

    if (!messagesBox) {
        return;
    }


    /*
       Initial Farhan message.
    */

    addMessage(
        "SYSTEM READY.\n\nAsk me something about Farhan.",
        "ai"
    );


    try {

        const response = await fetch(
            `${BACKEND_URL}?visitor_id=${encodeURIComponent(visitorId)}`
        );


        if (!response.ok) {

            throw new Error(
                `History request failed: ${response.status}`
            );
        }


        const data =
            await response.json();


        /*
           Add previous conversations.
        */

        (data.history || []).forEach(
            (item) => {

                if (item.question) {

                    addMessage(
                        item.question,
                        "user"
                    );
                }


                if (item.answer) {

                    addMessage(
                        item.answer,
                        "ai"
                    );
                }
            }
        );

    }

    catch (error) {

        console.error(
            "Could not load chat history:",
            error
        );
    }
}


/* ============================================================
   SEND QUESTION
   ============================================================ */

async function sendQuestion() {

    if (!questionInput) {
        return;
    }


    const question =
        questionInput.value.trim();


    /* Don't send empty messages */

    if (!question) {
        return;
    }


    /* --------------------------------------------------------
       Show user's message immediately
       -------------------------------------------------------- */

    addMessage(
        question,
        "user"
    );


    /* Clear input */

    questionInput.value = "";


    /* --------------------------------------------------------
       Show processing message
       -------------------------------------------------------- */

    addMessage(
        "PROCESSING REQUEST...",
        "ai"
    );


    try {

        const response =
            await fetch(
                BACKEND_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        question: question,

                        visitor_id:
                            visitorId,

                        name:
                            localStorage.getItem(
                                "visitorName"
                            ) || null
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                `Request failed: ${response.status}`
            );
        }


        const data =
            await response.json();


        /* ----------------------------------------------------
           Remove PROCESSING REQUEST message
           ---------------------------------------------------- */

        const lastMessage =
            messagesBox?.lastElementChild;


        if (lastMessage) {
            lastMessage.remove();
        }


        /* ----------------------------------------------------
           Show Farhan's answer
           ---------------------------------------------------- */

        addMessage(
            data.reply || "No response received.",
            "ai"
        );

    }


    catch (error) {

        console.error(
            "Request failed:",
            error
        );


        /* Remove processing message */

        const lastMessage =
            messagesBox?.lastElementChild;


        if (lastMessage) {
            lastMessage.remove();
        }


        /* Show error */

        addMessage(
            "SYSTEM ERROR. PLEASE TRY AGAIN.",
            "ai"
        );
    }
}


/* ============================================================
   SEND BUTTON
   ============================================================ */

if (sendButton) {

    sendButton.addEventListener(
        "click",
        sendQuestion
    );
}


/* ============================================================
   ENTER KEY TO SEND
   ============================================================ */

if (questionInput) {

    questionInput.addEventListener(
        "keydown",
        (event) => {

            if (event.key === "Enter") {

                event.preventDefault();

                sendQuestion();
            }
        }
    );
}


/* ============================================================
   MOBILE MENU
   ============================================================ */

if (
    mobileMenuButton &&
    mobileMenu
) {

    mobileMenuButton.addEventListener(
        "click",
        () => {

            mobileMenu.classList.toggle(
                "active"
            );
        }
    );


    mobileMenu
        .querySelectorAll("a")
        .forEach(
            (link) => {

                link.addEventListener(
                    "click",
                    () => {

                        mobileMenu.classList.remove(
                            "active"
                        );
                    }
                );
            }
        );
}


/* ============================================================
   PAGE START
   ============================================================ */

showNamePopupIfFirstVisit();

loadHistory();