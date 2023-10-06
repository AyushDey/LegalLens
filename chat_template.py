css = '''
<style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }

    .chat-message p {
        font-size: smaller;
        text-align: center;
        color: orange;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .chat-message.user {
        background-color: #2b313e;
        flex-direction: row-reverse; /* Reverse the order of flex items */
        justify-content: flex-start;
    }

    .chat-message.bot {
        background-color: #475063;
        flex-direction: row;
        justify-content: flex-start;
    }

    .chat-message .avatar img {
        max-width: 78px;
        max-height: 78px;
        border-radius: 50%;
        object-fit: cover;
        
    }

    .chat-message .message {
        width: 80%;
        padding: 0 1.5rem;
        color: #fff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .chat-message.user p {
        color: yellow;
    }

    .output {
            display: flex;
            flex-direction: row;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 10px;
            background-color: #030136;
            text-align: left;
            justify-content: left;
            align-items: center;
            border: 2px solid #FDB674;
            box-shadow:inset;
        }

    .output p {
        padding: 10px;
        margin: 2px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #FDB674;        
    }    

    .st-emotion-cache-10oheav .eczjsme4 {
        background-color: #010027;
    }

'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/h8VjckN/law-firm-logo-law-firm-logo-vector-23219700.jpg"><br>
        <p>Bot</p>
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/X5ZbqgX/purple-user-icon-in-circle-thin-line-vector-23745268.jpg"><br>
        <p>User</p>
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
summarize_template = '''
<div class="output">
    <p>{{TXT}}</p>
</div>
'''