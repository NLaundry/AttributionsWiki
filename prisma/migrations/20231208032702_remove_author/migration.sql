/*
  Warnings:

  - You are about to drop the column `authorId` on the `Attribution` table. All the data in the column will be lost.
  - You are about to drop the column `authorId` on the `Belief` table. All the data in the column will be lost.
  - You are about to drop the column `authorId` on the `Factor` table. All the data in the column will be lost.

*/
-- DropForeignKey
ALTER TABLE "Attribution" DROP CONSTRAINT "Attribution_authorId_fkey";

-- DropForeignKey
ALTER TABLE "Belief" DROP CONSTRAINT "Belief_authorId_fkey";

-- DropForeignKey
ALTER TABLE "Factor" DROP CONSTRAINT "Factor_authorId_fkey";

-- AlterTable
ALTER TABLE "Attribution" DROP COLUMN "authorId";

-- AlterTable
ALTER TABLE "Belief" DROP COLUMN "authorId";

-- AlterTable
ALTER TABLE "Factor" DROP COLUMN "authorId";
