// Global data
let currentUser = {
    username: 'your_username',
    name: 'Your Name',
    bio: 'Welcome to my Instagram!',
    avatar: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=56&h=56&fit=crop&crop=face'
};

let posts = [];
let stories = [];
let suggestions = [];
let currentPage = 0;
let isLoading = false;

// Sample data
const avatarImages = [
    'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=56&h=56&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=56&h=56&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=56&h=56&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=56&h=56&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=56&h=56&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=56&h=56&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=56&h=56&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=56&h=56&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=56&h=56&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=56&h=56&fit=crop&crop=face'
];

const sampleUsers = [
    { username: 'travel_lover', name: 'Travel Enthusiast', avatar: avatarImages[0] },
    { username: 'art_gallery', name: 'Art Gallery', avatar: avatarImages[1] },
    { username: 'foodie_blog', name: 'Food Blogger', avatar: avatarImages[2] },
    { username: 'fitness_goals', name: 'Fitness Coach', avatar: avatarImages[3] },
    { username: 'book_worm', name: 'Book Lover', avatar: avatarImages[4] },
    { username: 'music_lover', name: 'Music Fan', avatar: avatarImages[5] },
    { username: 'photography_pro', name: 'Photographer', avatar: avatarImages[6] },
    { username: 'plant_parent', name: 'Plant Parent', avatar: avatarImages[7] },
    { username: 'tech_geek', name: 'Tech Enthusiast', avatar: avatarImages[8] },
    { username: 'pet_lover', name: 'Pet Lover', avatar: avatarImages[9] }
];

const sampleImages = [
    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&h=600&fit=crop',
    'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&h=600&fit=crop',
    'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=600&h=600&fit=crop',
    'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=600&fit=crop',
    'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&h=600&fit=crop',
    'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=600&fit=crop',
    'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=600&h=600&fit=crop',
    'https://images.unsplash.com/photo-1552053831-71594a27632d?w=600&h=600&fit=crop',
    'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=600&h=600&fit=crop',
    'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=600&h=600&fit=crop'
];

const sampleCaptions = [
    'Amazing sunset at the mountains! 🌅 #travel #nature #sunset',
    'New abstract piece I\'ve been working on! What do you think? 🎭 #art #abstract #creative',
    'Homemade pizza night! 🍕🔥 This margherita turned out perfectly! #pizza #homemade #foodie',
    'Morning workout complete! 💪 Ready to conquer the day! #fitness #motivation #workout',
    'Just finished this amazing book! 📖 Highly recommend! #books #reading #literature',
    'New song I\'ve been working on! 🎵 What do you think? #music #creative #songwriting',
    'Captured this beautiful moment today! 📸 #photography #nature #beauty',
    'My plant collection is growing! 🌱 #plants #nature #home',
    'Working on some new code! 💻 #programming #tech #coding',
    'Best friends forever! 🐕 #pets #love #friendship'
];

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    console.log('Initializing Instagram app...');
    loadStories();
    loadPosts();
    loadSuggestions();
    setupInfiniteScroll();
    setupEventListeners();
    setupSearch();
    console.log('App initialization complete!');
}

// Stories functionality
function loadStories() {
    stories = sampleUsers.map(user => ({
        ...user,
        viewed: Math.random() > 0.5,
        timestamp: new Date(Date.now() - Math.random() * 86400000)
    }));
    renderStories();
}

function renderStories() {
    const container = document.getElementById('storiesContainer');
    container.innerHTML = `
        <div class="story" onclick="addStory()">
            <div class="story-avatar">
                <img src="${currentUser.avatar}" alt="Your story">
            </div>
            <div class="story-username">your_story</div>
        </div>
        ${stories.map(story => `
            <div class="story ${story.viewed ? 'viewed' : ''}" onclick="viewStory('${story.username}')">
                <div class="story-avatar">
                    <img src="${story.avatar}" alt="Story avatar">
                </div>
                <div class="story-username">${story.username}</div>
            </div>
        `).join('')}
    `;
}

// Posts functionality
function loadPosts() {
    if (isLoading) return;
    
    isLoading = true;
    showLoading(true);

    setTimeout(() => {
        const newPosts = generatePosts(5);
        posts = [...posts, ...newPosts];
        renderPosts();
        showLoading(false);
        isLoading = false;
        currentPage++;
    }, 1000);
}

function generatePosts(count) {
    const newPosts = [];
    for (let i = 0; i < count; i++) {
        const user = sampleUsers[Math.floor(Math.random() * sampleUsers.length)];
        const imageUrl = sampleImages[Math.floor(Math.random() * sampleImages.length)];
        const caption = sampleCaptions[Math.floor(Math.random() * sampleCaptions.length)];
        
        newPosts.push({
            id: Date.now() + i,
            user: user,
            image: imageUrl,
            caption: caption,
            likes: Math.floor(Math.random() * 5000) + 100,
            comments: Math.floor(Math.random() * 200) + 10,
            timestamp: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000),
            liked: false,
            saved: false
        });
    }
    return newPosts;
}

function renderPosts() {
    const container = document.getElementById('postsContainer');
    container.innerHTML = posts.map(post => `
        <div class="post" data-post-id="${post.id}">
            <div class="post-header">
                <div class="post-user">
                    <div class="post-avatar">
                        <img src="${post.user.avatar}" alt="User avatar">
                    </div>
                    <div class="post-username" onclick="viewProfile('${post.user.username}')">${post.user.username}</div>
                </div>
                <i class="fas fa-ellipsis-h post-more" onclick="showPostOptions(${post.id})"></i>
            </div>
            <div class="post-image" onclick="viewPostDetail(${post.id})">
                <img src="${post.image}" alt="Post image">
            </div>
            <div class="post-actions">
                <div class="action-buttons">
                    <i class="${post.liked ? 'fas' : 'far'} fa-heart action-btn ${post.liked ? 'liked' : ''}" onclick="toggleLike(${post.id})"></i>
                    <i class="far fa-comment action-btn" onclick="viewPostDetail(${post.id})"></i>
                    <i class="far fa-paper-plane action-btn" onclick="sharePost(${post.id})"></i>
                    <i class="${post.saved ? 'fas' : 'far'} fa-bookmark action-btn" style="margin-left: auto;" onclick="toggleSave(${post.id})"></i>
                </div>
                <div class="likes" onclick="viewPostDetail(${post.id})">${formatNumber(post.likes)} likes</div>
                <div class="caption">
                    <strong>${post.user.username}</strong> ${post.caption}
                </div>
                <div class="comments" onclick="viewPostDetail(${post.id})">View all ${post.comments} comments</div>
                <div class="timestamp">${formatTimestamp(post.timestamp)}</div>
            </div>
        </div>
    `).join('');
}

// Suggestions functionality
function loadSuggestions() {
    suggestions = sampleUsers
        .filter(user => user.username !== currentUser.username)
        .sort(() => Math.random() - 0.5)
        .slice(0, 5)
        .map(user => ({
            ...user,
            followed: Math.random() > 0.7,
            followedBy: Math.random() > 0.5 ? `user${Math.floor(Math.random() * 1000)}` : null
        }));
    renderSuggestions();
}

function renderSuggestions() {
    const container = document.getElementById('suggestionsContainer');
    container.innerHTML = suggestions.map(suggestion => `
        <div class="suggestion">
            <div class="suggestion-avatar" onclick="viewProfile('${suggestion.username}')">
                <img src="${suggestion.avatar}" alt="Suggestion avatar">
            </div>
            <div class="suggestion-info">
                <div class="suggestion-username" onclick="viewProfile('${suggestion.username}')">${suggestion.username}</div>
                <div class="suggestion-followed">
                    ${suggestion.followedBy ? `Followed by ${suggestion.followedBy}` : 'New to Instagram'}
                </div>
            </div>
            <div class="follow-btn" onclick="toggleFollow('${suggestion.username}')">
                ${suggestion.followed ? 'Following' : 'Follow'}
            </div>
        </div>
    `);
}

// Interactive functions
function toggleLike(postId) {
    const post = posts.find(p => p.id === postId);
    if (post) {
        post.liked = !post.liked;
        post.likes += post.liked ? 1 : -1;
        renderPosts();
        showNotification(post.liked ? 'Post liked!' : 'Post unliked!');
    }
}

function toggleSave(postId) {
    const post = posts.find(p => p.id === postId);
    if (post) {
        post.saved = !post.saved;
        renderPosts();
        showNotification(post.saved ? 'Post saved!' : 'Post unsaved!');
    }
}

function toggleFollow(username) {
    const suggestion = suggestions.find(s => s.username === username);
    if (suggestion) {
        suggestion.followed = !suggestion.followed;
        renderSuggestions();
        showNotification(suggestion.followed ? `Following ${username}!` : `Unfollowed ${username}!`);
    }
}

function viewStory(username) {
    const story = stories.find(s => s.username === username);
    if (story) {
        story.viewed = true;
        renderStories();
        showNotification(`Viewing ${username}'s story!`);
    }
}

function addStory() {
    showNotification('Add story feature would open here!');
}

function viewProfile(username) {
    showNotification(`Viewing ${username}'s profile!`);
}

function viewPostDetail(postId) {
    const post = posts.find(p => p.id === postId);
    if (post) {
        const modal = document.getElementById('postDetailModal');
        const content = document.getElementById('postDetailContent');
        
        content.innerHTML = `
            <div class="post-detail-image">
                <img src="${post.image}" alt="Post image">
            </div>
            <div class="post-detail-info">
                <div class="post-detail-header">
                    <div class="post-user">
                        <div class="post-avatar">
                            <img src="${post.user.avatar}" alt="User avatar">
                        </div>
                        <div class="post-username">${post.user.username}</div>
                    </div>
                </div>
                <div class="post-detail-caption">
                    <strong>${post.user.username}</strong> ${post.caption}
                </div>
                <div class="post-detail-actions">
                    <div class="action-buttons">
                        <i class="${post.liked ? 'fas' : 'far'} fa-heart action-btn ${post.liked ? 'liked' : ''}" onclick="toggleLike(${post.id})"></i>
                        <i class="far fa-comment action-btn"></i>
                        <i class="far fa-paper-plane action-btn"></i>
                        <i class="${post.saved ? 'fas' : 'far'} fa-bookmark action-btn" style="margin-left: auto;" onclick="toggleSave(${post.id})"></i>
                    </div>
                    <div class="likes">${formatNumber(post.likes)} likes</div>
                    <div class="timestamp">${formatTimestamp(post.timestamp)}</div>
                </div>
                <div class="comment-section">
                    <textarea placeholder="Add a comment..." rows="2"></textarea>
                    <button class="post-comment-btn">Post</button>
                </div>
            </div>
        `;
        
        modal.style.display = 'block';
    }
}

function showPostOptions(postId) {
    showNotification(`Options for post ${postId} would open here!`);
}

function sharePost(postId) {
    showNotification(`Share post ${postId} feature would open here!`);
}

// Navigation functions
function setActiveTab(tab) {
    document.querySelectorAll('.nav-icon').forEach(icon => icon.classList.remove('active'));
    event.target.classList.add('active');
    
    switch(tab) {
        case 'home':
            refreshFeed();
            break;
        case 'messages':
            showNotification('Messages feature would open here!');
            break;
        case 'explore':
            showNotification('Explore page would open here!');
            break;
        case 'notifications':
            showNotification('Notifications would open here!');
            break;
    }
}

function refreshFeed() {
    posts = [];
    currentPage = 0;
    loadPosts();
    showNotification('Feed refreshed!');
}

// Modal functions
function showCreatePost() {
    document.getElementById('createPostModal').style.display = 'block';
    resetCreatePostForm();
}

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('previewImage').src = e.target.result;
            document.getElementById('uploadArea').style.display = 'none';
            document.getElementById('postPreview').style.display = 'block';
            document.getElementById('shareBtn').disabled = false;
        };
        reader.readAsDataURL(file);
    }
}

function createPost() {
    const caption = document.getElementById('postCaption').value;
    const previewImage = document.getElementById('previewImage').src;
    
    if (previewImage && caption.trim()) {
        const newPost = {
            id: Date.now(),
            user: currentUser,
            image: previewImage,
            caption: caption,
            likes: 0,
            comments: 0,
            timestamp: new Date(),
            liked: false,
            saved: false
        };

        posts.unshift(newPost);
        renderPosts();
        closeModal('createPostModal');
        showNotification('Post created successfully!');
        resetCreatePostForm();
    }
}

function resetCreatePostForm() {
    document.getElementById('postCaption').value = '';
    document.getElementById('uploadArea').style.display = 'block';
    document.getElementById('postPreview').style.display = 'none';
    document.getElementById('shareBtn').disabled = true;
}

function showProfile() {
    document.getElementById('profileUsername').value = currentUser.username;
    document.getElementById('profileName').value = currentUser.name;
    document.getElementById('profileBio').value = currentUser.bio || '';
    document.getElementById('profileModal').style.display = 'block';
}

function updateProfile() {
    const newUsername = document.getElementById('profileUsername').value;
    const newName = document.getElementById('profileName').value;
    const newBio = document.getElementById('profileBio').value;

    if (newUsername && newName) {
        currentUser.username = newUsername;
        currentUser.name = newName;
        currentUser.bio = newBio;
        
        document.getElementById('currentUsername').textContent = newUsername;
        document.getElementById('currentName').textContent = newName;
        
        closeModal('profileModal');
        showNotification('Profile updated successfully!');
    }
}

function switchAccount() {
    const randomUser = sampleUsers[Math.floor(Math.random() * sampleUsers.length)];
    currentUser = { ...randomUser };
    
    document.getElementById('currentUsername').textContent = currentUser.username;
    document.getElementById('currentName').textContent = currentUser.name;
    
    const userAvatar = document.querySelector('.user-avatar img');
    if (userAvatar) {
        userAvatar.src = currentUser.avatar;
    }
    
    showNotification(`Switched to ${currentUser.username}!`);
}

function showAllSuggestions() {
    showNotification('All suggestions would open here!');
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Utility functions
function showLoading(show) {
    document.getElementById('loadingIndicator').style.display = show ? 'block' : 'none';
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatTimestamp(date) {
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 60) {
        return `${minutes} minutes ago`;
    } else if (hours < 24) {
        return `${hours} hours ago`;
    } else {
        return `${days} days ago`;
    }
}

function showNotification(message) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Search functionality
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase();
        if (query.length >= 2) {
            performSearch(query);
        }
    });
}

function performSearch(query) {
    const results = sampleUsers.filter(user => 
        user.username.toLowerCase().includes(query) ||
        user.name.toLowerCase().includes(query)
    );
    
    if (results.length > 0) {
        showNotification(`Found ${results.length} users matching "${query}"`);
    }
}

// Setup functions
function setupInfiniteScroll() {
    window.addEventListener('scroll', () => {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 1000) {
            loadPosts();
        }
    });
}

function setupEventListeners() {
    // Close modals when clicking outside
    window.addEventListener('click', (event) => {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });

    // Handle enter key in modals
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const createModal = document.getElementById('createPostModal');
            const profileModal = document.getElementById('profileModal');
            
            if (createModal.style.display === 'block') {
                createPost();
            } else if (profileModal.style.display === 'block') {
                updateProfile();
            }
        }
    });

    // Add keyboard shortcuts
    document.addEventListener('keydown', (event) => {
        // Ctrl/Cmd + R to refresh feed
        if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
            event.preventDefault();
            refreshFeed();
        }
        
        // Ctrl/Cmd + N for new post
        if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
            event.preventDefault();
            showCreatePost();
        }
        
        // Escape to close modals
        if (event.key === 'Escape') {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                if (modal.style.display === 'block') {
                    modal.style.display = 'none';
                }
            });
        }
    });

    // Add real-time updates simulation
    setInterval(() => {
        // Randomly add new stories
        if (Math.random() > 0.95) {
            addRandomStory();
        }
        
        // Randomly update like counts
        if (Math.random() > 0.98) {
            updateRandomLikes();
        }
    }, 5000);
}

// Additional dynamic features
function addRandomStory() {
    const randomUser = sampleUsers[Math.floor(Math.random() * sampleUsers.length)];
    const newStory = {
        ...randomUser,
        viewed: false,
        timestamp: new Date()
    };
    
    stories.unshift(newStory);
    if (stories.length > 10) {
        stories.pop();
    }
    renderStories();
    showNotification(`${randomUser.username} added a new story!`);
}

function updateRandomLikes() {
    if (posts.length > 0) {
        const randomPost = posts[Math.floor(Math.random() * posts.length)];
        const increment = Math.floor(Math.random() * 5) + 1;
        randomPost.likes += increment;
        renderPosts();
    }
} 