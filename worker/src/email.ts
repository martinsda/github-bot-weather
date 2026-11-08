import { createMimeMessage } from "mimetext/browser";
import { EmailMessage } from "cloudflare:email";
import type { Env, ForecastDay } from "./weather";

export async function maybeSendRainAlert(env: Env, dayZero: ForecastDay): Promise<void> {
	const threshold = Number(env.RAIN_EMAIL_THRESHOLD);
	if (dayZero.precipitationProbabilityMax < threshold) {
		return;
	}

	const msg = createMimeMessage();
	msg.setSender({ name: "Weather Bot", addr: env.EMAIL_FROM });
	msg.setRecipient(env.EMAIL_TO);
	msg.setSubject(`☔ High chance of rain today in ${env.CITY}`);
	msg.addMessage({
		contentType: "text/plain",
		data: [
			`Rain probability today in ${env.CITY}: ${dayZero.precipitationProbabilityMax}%`,
			`Expected precipitation: ${dayZero.precipitationSum} mm`,
			`Max. temp: ${dayZero.tempMax}ºC Min.: ${dayZero.tempMin}ºC`,
		].join("\n"),
	});

	const message = new EmailMessage(env.EMAIL_FROM, env.EMAIL_TO, msg.asRaw());
	await env.SEND_EMAIL.send(message);
}
