// chat.js

document.addEventListener("DOMContentLoaded", function () {
  // Sample data for demonstration
  const chatMessages = [
    { sender: "User", message: "Hello there!", timestamp: "10:00 AM" },
    {
      sender: "Bot",
      message: "Hi! How can I help you today?",
      timestamp: "10:01 AM",
    },
    {
      sender: "User",
      message: "I have a question about your services.",
      timestamp: "10:02 AM",
    },
    {
      sender: "Bot",
      message: "Sure, feel free to ask!",
      timestamp: "10:03 AM",
    },
    {
      sender: "User",
      message: "What are your pricing plans?",
      timestamp: "10:05 AM",
    },
    {
      sender: "Bot",
      message: "Our pricing plans start at $10/month.",
      timestamp: "10:06 AM",
    },
    { sender: "User", message: "Okay, thank you!", timestamp: "10:07 AM" },
  ];

  const chatContainer = document.getElementById("chat-container");

  // Function to add messages to the chat container
  function renderMessages(messages) {
    messages.forEach((message) => {
      const messageDiv = document.createElement("div");
      messageDiv.classList.add("message");

      messageDiv.innerHTML = `
        <p><strong>${message.sender}:</strong> ${message.message}</p>
        <p class="meta">${message.timestamp}</p>
      `;

      chatContainer.appendChild(messageDiv);
    });
  }

  // Render initial messages
  renderMessages(chatMessages);
});
