document.addEventListener("DOMContentLoaded", () => {
    const searchBtn = document.getElementById("searchBtn");
    const searchInput = document.getElementById("search");
    const songCards = document.getElementById("songCards");
    const youtubePlayer = document.getElementById("youtubePlayer");
    const meaningBtn = document.getElementById("meaningBtn");
    const wordInput = document.getElementById("word");
    const wordMeaningDiv = document.getElementById("wordMeaning");

    // Search for Spotify tracks
    searchBtn.addEventListener("click", async () => {
        const query = searchInput.value;
        if (query) {
            const response = await fetch("/search_spotify", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({ query }),
            });
            const tracks = await response.json();
            displayTracks(tracks);
        }
    });

    // Display the tracks
    function displayTracks(tracks) {
        songCards.innerHTML = ""; // Clear previous results
        tracks.forEach(track => {
            const songCard = document.createElement("div");
            songCard.classList.add("songCard");
            songCard.innerHTML = `
                <h3>${track.name}</h3>
                <p>${track.artist}</p>
                <button class="playBtn" data-query="${track.youtube_search_query}">Play</button>
            `;
            songCards.appendChild(songCard);
        });

        // Add event listeners for play buttons
        const playButtons = document.querySelectorAll(".playBtn");
        playButtons.forEach(button => {
            button.addEventListener("click", () => {
                const query = button.getAttribute("data-query");
                searchYouTube(query);
            });
        });
    }

    // Search for YouTube video
    async function searchYouTube(query) {
        const response = await fetch("/search_youtube", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({ query }),
        });
        const data = await response.json();
        youtubePlayer.src = data.video_url ? data.video_url.replace("watch?v=", "embed/") : "";
    }

    // Get word meaning
    meaningBtn.addEventListener("click", async () => {
        const word = wordInput.value;
        if (word) {
            const response = await fetch("/get_word_meaning", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({ word }),
            });
            const data = await response.json();
            wordMeaningDiv.textContent = data.meaning || "No definition found.";
        }
    });

    // Get lyrics when a play button is clicked (you can modify this based on your UI flow)
    async function getLyrics(artist, title) {
        const response = await fetch("/get_lyrics", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({ artist, title }),
        });
        const data = await response.json();
        const lyricsDiv = document.getElementById("lyrics");
        lyricsDiv.textContent = data.lyrics || "Lyrics not found.";
    }
});
