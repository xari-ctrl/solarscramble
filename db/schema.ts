import { pgTable, serial, text, integer, timestamp } from "drizzle-orm/pg-core";

export const leaderboardScores = pgTable("leaderboard_scores", {
  id: serial().primaryKey(),
  name: text().notNull(),
  score: integer().notNull(),
  createdAt: timestamp("created_at").defaultNow(),
});
