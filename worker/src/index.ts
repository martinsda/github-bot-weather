import { fetchCurrentWeather, fetchForecast, buildPosts, type Env } from "./weather";
import { pickRandomQuote } from "./quotes";
import { createSession, postToBluesky } from "./bluesky";
import { maybeSendRainAlert } from "./email";

export default {
	async scheduled(_event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
		const [weather, forecast] = await Promise.all([fetchCurrentWeather(env), fetchForecast(env)]);
		const quote = pickRandomQuote();

		const session = await createSession(env.BSKY_IDENTIFIER, env.BSKY_PASSWORD);
		const posts = buildPosts(weather, forecast, quote, env.CITY);
		for (const text of posts) {
			try {
				await postToBluesky(session, text);
			} catch (err) {
				console.error("Failed to post to Bluesky:", err);
			}
		}

		try {
			await maybeSendRainAlert(env, forecast[0]);
		} catch (err) {
			console.error("Failed to send rain alert email:", err);
		}
	},

	// Required by Wrangler's scheduled-event test harness (`--test-scheduled`); never
	// routable in production since `workers_dev` is disabled and no routes are bound.
	async fetch(): Promise<Response> {
		return new Response("Not found", { status: 404 });
	},
};
