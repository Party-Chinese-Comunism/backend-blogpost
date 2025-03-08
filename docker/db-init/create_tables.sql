-- Tabela users (plural)
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    profile_image VARCHAR(256)
);

-- Tabela posts (plural)
CREATE TABLE posts (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    image_url VARCHAR(256),
    created_at TIMESTAMP DEFAULT NOW(),
    update_at TIMESTAMP DEFAULT NOW(),  -- Removido ON UPDATE
    CONSTRAINT fk_posts_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Trigger para update_at
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_post_modtime 
BEFORE UPDATE ON posts 
FOR EACH ROW 
EXECUTE FUNCTION update_modified_column();

-- Tabela comments (plural)
CREATE TABLE comments (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL,
    CONSTRAINT fk_comments_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_comments_post FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE
);

-- Tabela favorites (plural mantido)
CREATE TABLE favorites (
    user_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL,
    PRIMARY KEY(user_id, post_id),
    CONSTRAINT fk_favorites_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_favorites_post FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE
);

-- Tabela likes (plural mantido)
CREATE TABLE likes (
    user_id BIGINT NOT NULL,
    comment_id BIGINT NOT NULL,
    PRIMARY KEY(user_id, comment_id),
    CONSTRAINT fk_likes_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_likes_comment FOREIGN KEY(comment_id) REFERENCES comments(id) ON DELETE CASCADE
);

-- Tabela followers (plural mantido)
CREATE TABLE followers (
    follower_id BIGINT NOT NULL,
    followed_id BIGINT NOT NULL,
    PRIMARY KEY(follower_id, followed_id),
    CONSTRAINT fk_followers_follower FOREIGN KEY(follower_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_followers_followed FOREIGN KEY(followed_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela revoked_tokens (plural)
CREATE TABLE revoked_tokens (
    id BIGSERIAL PRIMARY KEY,
    jti VARCHAR(120) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela refresh_tokens (plural)
CREATE TABLE refresh_tokens (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    jti VARCHAR(120) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    revoked BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_refresh_tokens_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);