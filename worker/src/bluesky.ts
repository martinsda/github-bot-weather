export interface BskySession {
	accessJwt: string;
	did: string;
}

export async function createSession(identifier: string, password: string): Promise<BskySession> {
	const response = await fetch("https://bsky.social/xrpc/com.atproto.server.createSession", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ identifier, password }),
	});
	if (!response.ok) {
		throw new Error(`Bluesky login failed: ${response.status} ${await response.text()}`);
	}
	const data = (await response.json()) as any;
	return { accessJwt: data.accessJwt, did: data.did };
}

export async function postToBluesky(session: BskySession, text: string): Promise<void> {
	const response = await fetch("https://bsky.social/xrpc/com.atproto.repo.createRecord", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			Authorization: `Bearer ${session.accessJwt}`,
		},
		body: JSON.stringify({
			repo: session.did,
			collection: "app.bsky.feed.post",
			record: {
				$type: "app.bsky.feed.post",
				text,
				createdAt: new Date().toISOString(),
			},
		}),
	});
	if (!response.ok) {
		throw new Error(`Bluesky post failed: ${response.status} ${await response.text()}`);
	}
}
