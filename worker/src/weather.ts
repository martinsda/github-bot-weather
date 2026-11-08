export interface Env {
	CITY: string;
	OPEN_METEO_CITY_LAT: string;
	OPEN_METEO_CITY_LONG: string;
	EMAIL_FROM: string;
	EMAIL_TO: string;
	RAIN_EMAIL_THRESHOLD: string;
	OPENWEATHER_API_KEY: string;
	BSKY_IDENTIFIER: string;
	BSKY_PASSWORD: string;
	SEND_EMAIL: SendEmail;
}

export interface CurrentWeather {
	description: string;
	temperature: number;
	tempMin: number;
	tempMax: number;
	windSpeed: number;
	windDeg: number;
	windKmph: number;
}

export interface ForecastDay {
	date: Date;
	tempMax: number;
	tempMin: number;
	precipitationSum: number;
	precipitationProbabilityMax: number;
	windSpeedMax: number;
	windGustsMax: number;
	windDirectionDominant: number;
}

export async function fetchCurrentWeather(env: Env): Promise<CurrentWeather> {
	const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(env.CITY)}&appid=${env.OPENWEATHER_API_KEY}&units=metric`;
	const response = await fetch(url);
	if (!response.ok) {
		throw new Error(`Failed to get weather data: ${response.status}`);
	}
	const data = (await response.json()) as any;
	const windSpeed = data.wind.speed;
	return {
		description: data.weather[0].description,
		temperature: data.main.temp,
		tempMin: data.main.temp_min,
		tempMax: data.main.temp_max,
		windSpeed,
		windDeg: data.wind.deg,
		windKmph: Math.round(windSpeed * 3.6 * 10) / 10,
	};
}

export async function fetchForecast(env: Env): Promise<ForecastDay[]> {
	const daily = [
		"temperature_2m_max",
		"temperature_2m_min",
		"precipitation_sum",
		"precipitation_probability_max",
		"wind_speed_10m_max",
		"wind_gusts_10m_max",
		"wind_direction_10m_dominant",
	].join(",");
	const url = `https://api.open-meteo.com/v1/forecast?latitude=${env.OPEN_METEO_CITY_LAT}&longitude=${env.OPEN_METEO_CITY_LONG}&daily=${daily}`;
	const response = await fetch(url);
	if (!response.ok) {
		throw new Error(`Failed to get forecast data: ${response.status}`);
	}
	const data = (await response.json()) as any;
	const days: ForecastDay[] = [];
	// Only days 0-3 are used by the Bluesky posts (matches today's weather.yml).
	for (let i = 0; i <= 3; i++) {
		days.push({
			date: new Date(data.daily.time[i]),
			tempMax: data.daily.temperature_2m_max[i],
			tempMin: data.daily.temperature_2m_min[i],
			precipitationSum: data.daily.precipitation_sum[i],
			precipitationProbabilityMax: data.daily.precipitation_probability_max[i],
			windSpeedMax: data.daily.wind_speed_10m_max[i],
			windGustsMax: data.daily.wind_gusts_10m_max[i],
			windDirectionDominant: data.daily.wind_direction_10m_dominant[i],
		});
	}
	return days;
}

function formatRain(precipitationSum: number): string {
	return precipitationSum > 0 ? `Rain: ${round1(precipitationSum)} mm` : "No rain";
}

function formatWind(day: ForecastDay): string {
	return `Wind: ${Math.trunc(day.windSpeedMax)} up to ${Math.trunc(day.windGustsMax)} km/h ${Math.round(day.windDirectionDominant)}º`;
}

function round1(value: number): number {
	return Math.round(value * 10) / 10;
}

const WEEKDAY_FORMAT = new Intl.DateTimeFormat("en-US", { weekday: "short", timeZone: "UTC" });

export function buildPosts(weather: CurrentWeather, forecast: ForecastDay[], quote: string, city: string): string[] {
	const [day0, day1, day2, day3] = forecast;
	const rainProb0 = day0.precipitationProbabilityMax > 0 ? `${round1(day0.precipitationProbabilityMax)}%` : "0%";

	const quotePost = `Quote of the day 💬💭:\n${quote}.`;

	const forecastPost = [
		`#Forecast for #${city} 🏙️:`,
		`${WEEKDAY_FORMAT.format(day1.date)} 🗓️:`,
		`Max. temp: ${round1(day1.tempMax)} Cº Min.: ${round1(day1.tempMin)} Cº ${formatRain(day1.precipitationSum)} ${formatWind(day1)}`,
		`${WEEKDAY_FORMAT.format(day2.date)} 🗓️:`,
		`Max. temp: ${round1(day2.tempMax)} Cº Min.: ${round1(day2.tempMin)} Cº ${formatRain(day2.precipitationSum)} ${formatWind(day2)}`,
		`${WEEKDAY_FORMAT.format(day3.date)} 🗓️:`,
		`Max. temp: ${round1(day3.tempMax)} Cº Min.: ${round1(day3.tempMin)} Cº ${formatRain(day3.precipitationSum)} ${formatWind(day3)}`,
	].join("\n");

	const todayPost = [
		`Forecast for #${city} 🏙️:`,
		`Today 🗓️:`,
		`#Rain probability: ${rainProb0}`,
		`Max. temp: ${round1(day0.tempMax)} Cº Min.: ${round1(day0.tempMin)} Cº ${formatRain(day0.precipitationSum)} ${formatWind(day0)}`,
	].join("\n");

	const currentPost = [
		`Currently in #${city}: ${weather.description}`,
		`#Temperature: ${weather.temperature} Cº / Max.: ${round1(day0.tempMax)} Cº Min.: ${round1(day0.tempMin)} Cº`,
		`#Wind speed: ${weather.windSpeed} meters/sec => ${weather.windKmph} km/h`,
		`#Wind direction: ${weather.windDeg}º`,
	].join("\n");

	return [quotePost, forecastPost, todayPost, currentPost];
}
